from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db

async def build_settings_view(user_id: int):
    user_data = await db.get_user_data(user_id)
    metadata_status = user_data.get("metadata", "Off")
    prefix = user_data.get("prefix", None)
    suffix = user_data.get("suffix", None)
    caption = user_data.get("caption", None)
    thumb = user_data.get("file_id", None)
    dump_channel = user_data.get("dump_channel", None)
    
    text = (
        "⚙️ **Your User Preferences & Settings**\n\n"
        f"🏷 **Metadata Injection:** `{'✅ Enabled (On)' if metadata_status == 'On' else '❌ Disabled (Off)'}`\n"
        f"🔤 **Custom Prefix:** `{prefix or 'Not Set'}`\n"
        f"🔤 **Custom Suffix:** `{suffix or 'Not Set'}`\n"
        f"📝 **Custom Caption:** `{'✅ Set' if caption else '❌ Default'}`\n"
        f"🖼 **Custom Thumbnail:** `{'✅ Saved' if thumb else '❌ Default'}`\n"
        f"📥 **Dump Channel:** `{dump_channel or 'Not Set'}`\n\n"
        "Tap the buttons below to configure each option or toggle metadata directly:"
    )

    buttons = [
        [
            InlineKeyboardButton(
                f"Metadata: {'🟢 ON' if metadata_status == 'On' else '🔴 OFF'}",
                callback_data="toggle_setting_metadata"
            )
        ],
        [
            InlineKeyboardButton("📝 Caption", callback_data="caption"),
            InlineKeyboardButton("🖼 Thumbnail", callback_data="thumbnail")
        ],
        [
            InlineKeyboardButton("🔤 Prefix / Suffix", callback_data="suffix_prefix"),
            InlineKeyboardButton("📥 Dump Channel", callback_data="dump")
        ],
        [
            InlineKeyboardButton("🏷 Set Metadata Details", callback_data="metainfo")
        ],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("✖️ Close", callback_data="close")
        ]
    ]
    return text, InlineKeyboardMarkup(buttons)


@Client.on_message(filters.private & filters.command("settings"))
async def user_settings_command(client, message):
    text, markup = await build_settings_view(message.from_user.id)
    await message.reply_text(text=text, reply_markup=markup, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r"^toggle_setting_metadata$"))
async def toggle_metadata_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    current = await db.get_metadata(user_id)
    new_status = "Off" if current == "On" else "On"
    await db.set_metadata(user_id, new_status)
    
    text, markup = await build_settings_view(user_id)
    await query.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)
    await query.answer(f"Metadata is now {new_status}")


@Client.on_callback_query(filters.regex(r"^refresh_settings$"))
async def refresh_settings_callback(client, query: CallbackQuery):
    text, markup = await build_settings_view(query.from_user.id)
    await query.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)
    await query.answer("Settings refreshed!")
