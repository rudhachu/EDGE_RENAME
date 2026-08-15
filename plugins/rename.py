import shutil
import uuid
import os
import time
from pathlib import Path
from PIL import Image

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from config import Config
from helper.utils import (
    progress_for_pyrogram, 
    convert, 
    humanbytes, 
    split_name_and_ext, 
    format_custom_filename, 
    run_async_ffmpeg,
    TASK_CANCELLATION
)
from helper.database import db
from pyrogram import StopTransmission


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = getattr(file, "file_name", "file")

    if file.file_size > 2000 * 1024 * 1024:
        return await message.reply_text("Sorry, this bot currently supports uploading files up to 2GB.")

    try:
        await message.reply_text(
            text=f"**Please Enter New Filename...**\n\n**Current File Name** :- `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text(
            text=f"**Please Enter New Filename**\n\n**Current File Name** :- `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except Exception:
        pass


@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.reply_markup and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text.strip()
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        orig_filename = getattr(media, "file_name", "file.mkv")

        # Normalize extension if user didn't provide one
        _, orig_ext = split_name_and_ext(orig_filename)
        if not orig_ext:
            orig_ext = ".mkv" if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT] else ".mp3"

        if not Path(new_name).suffix:
            new_name = f"{new_name}{orig_ext}"

        await reply_message.delete()

        button = [[InlineKeyboardButton("📁 Document", callback_data="upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Video", callback_data="upload_video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Audio", callback_data="upload_audio")])

        await message.reply(
            text=f"**Select The Output File Type**\n\n**File Name :-** `{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )


@Client.on_callback_query(filters.regex(r"^cancel_"))
async def cancel_task_callback(bot, update):
    task_id = update.data.split("_", 1)[1]
    TASK_CANCELLATION[task_id] = True
    await update.answer("🛑 Cancelling process...", show_alert=True)
    try:
        await update.message.edit("🛑 **Process cancelled by user.**")
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r"^upload_"))
async def doc(bot, update):
    user_id = update.from_user.id
    prefix = await db.get_prefix(user_id)
    suffix = await db.get_suffix(user_id)
    raw_text = update.message.text or ""
    
    # Extract filename from header
    if "File Name :-" in raw_text:
        base_name = raw_text.split("File Name :-")[1].strip(" `\n")
    elif ":-" in raw_text:
        base_name = raw_text.split(":-")[1].strip(" `\n")
    else:
        base_name = "renamed_file.mkv"

    # Safely apply prefix/suffix without mangling extensions
    new_filename = format_custom_filename(base_name, prefix=prefix, suffix=suffix)

    # Create isolated sandboxed directory and cancellation tracking for this task
    task_id = uuid.uuid4().hex[:8]
    TASK_CANCELLATION[task_id] = False
    task_dir = Path(f"downloads/task_{task_id}")
    task_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = task_dir / new_filename
    temp_output_file = task_dir / f"meta_{new_filename}"
    ph_path = None
    
    file = update.message.reply_to_message
    ms = await update.message.edit("`Trying To Download...`")

    try:
        path = await bot.download_media(
            message=file, 
            file_name=str(file_path), 
            progress=progress_for_pyrogram,
            progress_args=("`Download Started....`", ms, time.time(), task_id)
        )
        
        if TASK_CANCELLATION.get(task_id):
            return await ms.edit("🛑 **Process was cancelled.**")

        if not path or not file_path.exists():
            return await ms.edit("❌ Failed to download media file.")

        # Check and apply metadata
        user_metadata_enabled = await db.get_metadata(user_id)
        if user_metadata_enabled == "On" and not TASK_CANCELLATION.get(task_id):
            title = await db.get_title(user_id)
            author = await db.get_author(user_id)
            artist = await db.get_artist(user_id)
            video = await db.get_video(user_id)
            audio = await db.get_audio(user_id)
            subtitle = await db.get_subtitle(user_id)

            metadata_log = (
                f"🎯 **Applying Metadata:**\n"
                f"├ **File:** `{new_filename}`\n"
                f"├ **Title:** `{title or 'Not set'}`\n"
                f"├ **Author:** `{author or 'Not set'}`\n"
                f"├ **Artist:** `{artist or 'Not set'}`\n"
                f"├ **Video Title:** `{video or 'Not set'}`\n"
                f"├ **Audio Title:** `{audio or 'Not set'}`\n"
                f"└ **Subtitle:** `{subtitle or 'Not set'}`"
            )
            await ms.edit(f"⚡️ **Adding Metadata...**\n\n{metadata_log}")

            metadata_command = [
                'ffmpeg',
                '-i', str(file_path),
                '-metadata', f'title={title or ""}',
                '-metadata', f'artist={artist or ""}',
                '-metadata', f'author={author or ""}',
                '-metadata:s:v', f'title={video or ""}',
                '-metadata:s:a', f'title={audio or ""}',
                '-metadata:s:s', f'title={subtitle or ""}',
                '-map', '0',
                '-c', 'copy',
                '-loglevel', 'error',
                '-y',
                str(temp_output_file)
            ]

            returncode, stdout, stderr = await run_async_ffmpeg(metadata_command)
            if returncode == 0 and temp_output_file.exists():
                shutil.move(str(temp_output_file), str(file_path))
            else:
                print(f"FFmpeg error: {stderr}")

        if TASK_CANCELLATION.get(task_id):
            return await ms.edit("🛑 **Process was cancelled.**")

        # Extract duration
        duration = 0
        try:
            metadata = extractMetadata(createParser(str(file_path)))
            if metadata and metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception:
            pass

        # Prepare Caption
        media = getattr(file, file.media.value)
        c_caption = await db.get_caption(user_id)
        c_thumb = await db.get_thumbnail(user_id)

        if c_caption:
            try:
                caption = c_caption.format(
                    filename=new_filename, 
                    filesize=humanbytes(media.file_size),
                    duration=convert(duration)
                )
            except Exception as e:
                return await ms.edit(text=f"Your Caption Error: ({e})")
        else:
            caption = f"**{new_filename}**"
        
        logcaption = f"**{new_filename}**\nUploaded by {update.from_user.mention()}"

        # Thumbnail processing
        if c_thumb or (hasattr(media, 'thumbs') and media.thumbs):
            try:
                thumb_target = task_dir / "thumb.jpg"
                if c_thumb:
                    downloaded_thumb = await bot.download_media(c_thumb, file_name=str(thumb_target))
                else:
                    downloaded_thumb = await bot.download_media(media.thumbs[0].file_id, file_name=str(thumb_target))
                
                if downloaded_thumb and Path(downloaded_thumb).exists():
                    ph_path = str(thumb_target)
                    with Image.open(ph_path) as img:
                        img = img.convert("RGB")
                        img = img.resize((320, 320))
                        img.save(ph_path, "JPEG")
            except Exception as e:
                print(f"Thumbnail processing error: {e}")
                ph_path = None

        await ms.edit("`Trying To Upload....`")
        upload_type = update.data.split("_")[1]

        uploaded_message = None
        if upload_type == "document":
            uploaded_message = await bot.send_document(
                update.message.chat.id,
                document=str(file_path),
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time(), task_id)
            )
        elif upload_type == "video":
            uploaded_message = await bot.send_video(
                update.message.chat.id,
                video=str(file_path),
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time(), task_id)
            )
        elif upload_type == "audio":
            uploaded_message = await bot.send_audio(
                update.message.chat.id,
                audio=str(file_path),
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time(), task_id)
            )

        # Handle dump channel copies
        if uploaded_message and not TASK_CANCELLATION.get(task_id):
            user_dump = await db.get_dump_channel(user_id)
            if user_dump:
                try:
                    await bot.copy_message(
                        chat_id=user_dump,
                        from_chat_id=uploaded_message.chat.id,
                        message_id=uploaded_message.id,
                        caption=caption
                    )
                except Exception as e:
                    print(f"Error copying to user dump channel: {e}")

            if Config.DUMP_CHANNEL:
                try:
                    await bot.copy_message(
                        chat_id=Config.DUMP_CHANNEL,
                        from_chat_id=uploaded_message.chat.id,
                        message_id=uploaded_message.id,
                        caption=logcaption
                    )
                except Exception as e:
                    print(f"Error copying to bot dump channel: {e}")

        await ms.delete()

    except StopTransmission:
        try:
            await ms.edit("🛑 **Process was successfully cancelled.**")
        except Exception:
            pass
    except Exception as e:
        if TASK_CANCELLATION.get(task_id):
            try:
                await ms.edit("🛑 **Process was cancelled.**")
            except Exception:
                pass
        else:
            await ms.edit(f"❌ **Error:** `{e}`")
    finally:
        # Cleanup cancellation flag and sandbox
        TASK_CANCELLATION.pop(task_id, None)
        shutil.rmtree(task_dir, ignore_errors=True)
