import os
import xml.etree.ElementTree as ET

# Pre-translated dictionaries for the main UI strings
TRANSLATIONS = {
    "es": {
        "Multilingual File Organizer": "Organizador de Archivos Multilingüe",
        "Language:": "Idioma:",
        "Source folder...": "Carpeta de origen...",
        "Browse": "Examinar",
        "Source folder:": "Carpeta de origen:",
        "Destination folder...": "Carpeta de destino...",
        "Destination folder:": "Carpeta de destino:",
        "Move files (uncheck = copy)": "Mover archivos (desmarcar = copiar)",
        "Preview only (dry run)": "Solo vista previa (simulación)",
        "Start Sorting": "Iniciar clasificación",
        "Select source folder": "Seleccionar carpeta de origen",
        "Select destination folder": "Seleccionar carpeta de destino",
        "Missing info": "Información faltante",
        "Please select both folders.": "Por favor seleccione ambas carpetas.",
        "Done!\n\nMoved: {}\nSkipped: {}": "¡Hecho!\n\nMovidos: {}\nOmitidos: {}",
        "\nErrors: {}": "\nErrores: {}",
        "Finished": "Terminado",
        "Error": "Error"
    },
    "fr": {
        "Multilingual File Organizer": "Organisateur de Fichiers Multilingue",
        "Language:": "Langue :",
        "Source folder...": "Dossier source...",
        "Browse": "Parcourir",
        "Source folder:": "Dossier source :",
        "Destination folder...": "Dossier de destination...",
        "Destination folder:": "Dossier de destination :",
        "Move files (uncheck = copy)": "Déplacer les fichiers (décocher = copier)",
        "Preview only (dry run)": "Aperçu uniquement",
        "Start Sorting": "Démarrer le tri",
        "Select source folder": "Sélectionner le dossier source",
        "Select destination folder": "Sélectionner le dossier de destination",
        "Missing info": "Informations manquantes",
        "Please select both folders.": "Veuillez sélectionner les deux dossiers.",
        "Done!\n\nMoved: {}\nSkipped: {}": "Terminé !\n\nDéplacés : {}\nIgnorés : {}",
        "\nErrors: {}": "\nErreurs : {}",
        "Finished": "Terminé",
        "Error": "Erreur"
    },
    "de": {
        "Multilingual File Organizer": "Mehrsprachiger Dateiorganisator",
        "Language:": "Sprache:",
        "Source folder...": "Quellordner...",
        "Browse": "Durchsuchen",
        "Source folder:": "Quellordner:",
        "Destination folder...": "Zielordner...",
        "Destination folder:": "Zielordner:",
        "Move files (uncheck = copy)": "Dateien verschieben (deaktivieren = kopieren)",
        "Preview only (dry run)": "Nur Vorschau (Testlauf)",
        "Start Sorting": "Sortierung starten",
        "Select source folder": "Quellordner auswählen",
        "Select destination folder": "Zielordner auswählen",
        "Missing info": "Fehlende Informationen",
        "Please select both folders.": "Bitte wählen Sie beide Ordner aus.",
        "Done!\n\nMoved: {}\nSkipped: {}": "Fertig!\n\nVerschoben: {}\nÜbersprungen: {}",
        "\nErrors: {}": "\nFehler: {}",
        "Finished": "Fertig",
        "Error": "Fehler"
    },
    "ar": {
        "Multilingual File Organizer": "منظم الملفات متعدد اللغات",
        "Language:": "اللغة:",
        "Source folder...": "مجلد المصدر...",
        "Browse": "تصفح",
        "Source folder:": "مجلد المصدر:",
        "Destination folder...": "مجلد الوجهة...",
        "Destination folder:": "مجلد الوجهة:",
        "Move files (uncheck = copy)": "نقل الملفات (إلغاء التحديد = نسخ)",
        "Preview only (dry run)": "معاينة فقط",
        "Start Sorting": "ابدأ الفرز",
        "Select source folder": "اختر مجلد المصدر",
        "Select destination folder": "اختر مجلد الوجهة",
        "Missing info": "معلومات ناقصة",
        "Please select both folders.": "الرجاء اختيار كلا المجلدين.",
        "Done!\n\nMoved: {}\nSkipped: {}": "تم!\n\nتم النقل: {}\nتم التخطي: {}",
        "\nErrors: {}": "\nأخطاء: {}",
        "Finished": "انتهى",
        "Error": "خطأ"
    },
    "zh-CN": {
        "Multilingual File Organizer": "多语言文件整理器",
        "Language:": "语言:",
        "Source folder...": "源文件夹...",
        "Browse": "浏览",
        "Source folder:": "源文件夹:",
        "Destination folder...": "目标文件夹...",
        "Destination folder:": "目标文件夹:",
        "Move files (uncheck = copy)": "移动文件 (取消勾选=复制)",
        "Preview only (dry run)": "仅预览 (试运行)",
        "Start Sorting": "开始整理",
        "Select source folder": "选择源文件夹",
        "Select destination folder": "选择目标文件夹",
        "Missing info": "信息缺失",
        "Please select both folders.": "请选择两个文件夹。",
        "Done!\n\nMoved: {}\nSkipped: {}": "完成！\n\n已移动: {}\n已跳过: {}",
        "\nErrors: {}": "\n错误: {}",
        "Finished": "完成",
        "Error": "错误"
    }
}

def main():
    base_ts_path = "ui/translations/app_en.ts"
    if not os.path.exists(base_ts_path):
        print("Error: app_en.ts not found.")
        return

    for lang_code, dict_translations in TRANSLATIONS.items():
        print(f"\n--- Translating to {lang_code} ---")
        
        tree = ET.parse(base_ts_path)
        root = tree.getroot()
        root.set("language", lang_code)
        
        for context in root.findall("context"):
            for message in context.findall("message"):
                source = message.find("source").text
                translation_node = message.find("translation")
                
                if source and source in dict_translations:
                    translation_node.text = dict_translations[source]
                    if "type" in translation_node.attrib:
                        del translation_node.attrib["type"]
                    print(f"✓ {source} -> {dict_translations[source]}")

        output_path = f"ui/translations/app_{lang_code}.ts"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()