# Custom Translations

This folder allows you to add custom translations or override existing translations for the Square Root Calculator.

## How to Add Custom Translations

1. Create a JSON file with the language code as the filename (e.g., `de.json` for German, `fr.json` for French)
2. Add translation keys and values in JSON format
3. **Important**: Include the `_language_name` key to specify how your language appears in the menu
4. Restart the application or use **Language → Reload Translations** to load the new translations

## File Format

The JSON file should contain key-value pairs where:
- **Key**: Translation identifier (e.g., `app_title`, `calculate_button`)
- **Value**: Translated text in your language

**Special Key:**
- `_language_name` - The display name of your language in the Language menu (e.g., "Deutsch", "Français")

### Example: German Translation (`de.json`)

```json
{
  "_language_name": "Deutsch",
  "app_title": "Quadratwurzel-Rechner",
  "calculate_button": "Berechnen",
  "clear_button": "Löschen",
  "result_label": "Ergebnis",
  "mode_real": "Reelle Zahlen",
  "mode_complex": "Komplexe Zahlen"
}
```

## Available Translation Keys

Here are the main translation keys you can customize:

### Special Keys
- `_language_name` - **Required**: Display name of the language in the menu

### Application
- `app_title` - Application window title
- `error_title` - Error dialog title

### Input/Output
- `input_label` - Input field label
- `real_part_label` - Real part input label (complex mode)
- `imag_part_label` - Imaginary part input label (complex mode)
- `result_label` - Results section title
- `history_label` - History panel title

### Buttons
- `calculate_button` - Calculate button
- `clear_button` - Clear button
- `clear_history_button` - Clear history button

### Modes
- `mode_real` - Real numbers tab
- `mode_complex` - Complex numbers tab

### Precision
- `precision_control` - Precision control section title
- `precision_label` - Precision label
- `exact_value` - Exact precision field label

### Results
- `roots_label` - Roots section title
- `root_positive` - Positive root label
- `root_negative` - Negative root label
- `representations_label` - Representations section title
- `decimal_repr` - Decimal representation label
- `scientific_repr` - Scientific notation label
- `fraction_repr` - Fraction approximation label

### Menu Items
- `settings` - Settings menu
- `theme` - Theme submenu
- `theme_light` - Light theme option
- `theme_dark` - Dark theme option
- `language_menu` - Language menu
- `reload_translations` - Reload translations option
- `check_updates` - Check for updates option
- `help` - Help menu
- `about` - About dialog

### Messages
- `update_available` - Update notification title
- `update_message` - Update notification message (use `{}` for version placeholders)
- `skip_update` - Skip update button
- `download_update` - Download update button
- `no_update` - No update available message
- `translations_reloaded` - Translations reloaded confirmation

### Errors
- `invalid_input` - Invalid input error message
- `negative_real` - Negative real number error
- `calculation_error` - General calculation error (use `{}` for error details)
- `precision_too_low` - Precision too low error (use `{}` for required precision)
- `precision_error_generic` - Generic precision error (use `{}` for current and required precision)

## Overriding Existing Translations

You can also override existing English or Russian translations by creating `en.json` or `ru.json` files with only the keys you want to change.

### Example: Custom English (`en.json`)

```json
{
  "app_title": "My Custom Square Root Calculator",
  "calculate_button": "Compute Now!"
}
```

## Alternative Location

You can also place custom translations in:
```
~/.square_root_calculator/translations/
```

This is useful for system-wide custom translations that persist across updates.

## Reloading Translations

After adding or modifying translation files:
1. Use **Language → Reload Translations** menu option
2. Or restart the application

## Example Translation File

See `de.json.example` in this folder for a sample German translation file.
