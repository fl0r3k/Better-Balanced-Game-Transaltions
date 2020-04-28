import pandas as pd

lang_files = {
    'en_US': 'english.xml',
    'fr_FR': 'french.xml',
    'ru_RU': 'russian.xml',
    'pl_PL': 'polish.xml',
    'ko_KR': 'korean.xml',
    'ja_JP': 'japanese.xml'
}

langs = ['en_US', 'fr_FR', 'pl_PL', 'ru_RU', 'ko_KR']


def get_data():
    xlsx = pd.ExcelFile('translations.xlsx')
    metadata_frame = pd.read_excel(xlsx, 'metadata', index_col=0)
    metadata_frame.sort_values(inplace=True,
                               by=['Section1', 'Section2', 'Section3', 'Tag'], na_position='first')
    
    default_translations_frame = pd.read_excel(xlsx, 'en_US', index_col=0)

    print(metadata_frame)
    for lang in langs:
        lang_frame = pd.read_excel(xlsx, lang, index_col=0)
        with open('lang/' + lang_files[lang], 'w', encoding='utf-8') as f:

            print('\nProcesing ' + lang + ' file')

            wirte_header(f)
            current_section_1 = ''
            current_section_2 = ''
            current_section_3 = ''
            
            for tag, row in metadata_frame.iterrows():
                
                section_1 = row['Section1']
                section_2 = row['Section2']
                section_3 = row['Section3']

                if current_section_1 != section_1:
                    current_section_1 = section_1
                    write_section_header_1(f, current_section_1)

                if current_section_2 != section_2:
                    current_section_2 = section_2
                    write_section_header_2(f, current_section_2)

                if current_section_3 != section_3:
                    current_section_3 = section_3
                    write_section_header_3(f, current_section_3)

                if tag in lang_frame.index:
                    text = lang_frame.at[tag, 'Text']
                    if pd.isnull(text):
                        print(lang + ',' +  tag + ',MISSING_LANG_TRANSLATION')
                        try:
                            text = default_translations_frame.at[tag, 'Text']
                            if pd.isnull(text):
                                print(lang + ',' +  tag + ',MISSING_DEFAULT_TRANSLATION')
                                continue
                        except:
                            print(lang + ',' +  tag + ',MISSING_DEFAULT_TRANSLATION_TAG')
                            continue
                        
                else:
                    print(lang + ',' +  tag + ',MISSING_LANG_TAG')
                    try:
                        text = default_translations_frame.at[tag, 'Text']
                        if pd.isnull(text):
                            print(lang + ',' +  tag + ',MISSING_DEFAULT_TRANSLATION')
                            continue
                    except:
                        print(lang + ',' +  tag + ',MISSING_DEFAULT_TRANSLATION_TAG')
                        continue

                tabs = 2
                if not pd.isnull(section_2):
                    tabs = 3
                if not pd.isnull(section_3):
                    tabs = 4

                if row['Type'] == 'Replace':
                    wirte_replace(f, tag, lang, text, tabs)
                elif row['Type'] == 'Row':
                    wirte_row(f, tag, lang, text, tabs)


            wirte_footer(f)


def write_section_header_1(f, name):
    if not pd.isnull(name):
        f.write('\n\n\t\t<!-- ================ ')
        for c in name:
            f.write(c.upper() + ' ')
        f.write('================ -->\n')

def write_section_header_2(f, name):
    if not pd.isnull(name):
        f.write('\n\t\t\t<!-- ================ ' + name.title() + ' ================ -->\n')

def write_section_header_3(f, name):
    if not pd.isnull(name):
        f.write('\n\t\t\t\t<!-- ' + name.title() + ' -->\n')

def wirte_replace(f, tag, lang, text='', indentation=0):
    f.write(indent('<Replace Tag="' + tag +
            '" Language="' + lang + '">\n', 0 + indentation))
    f.write(indent('<Text>' + text + '</Text>\n', 1 + indentation))
    f.write(indent('</Replace>\n', 0 + indentation))


def wirte_row(f, tag, lang, text='', indentation=0):
    f.write(indent('<Row Tag="' + tag + '" Language="' +
            lang + '">\n', 0 + indentation))
    f.write(indent('<Text>' + text + '</Text>\n', 1 + indentation))
    f.write(indent('</Row>\n', 0 + indentation))


def wirte_header(f):
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<GameData>\n')
    f.write(indent('<LocalizedText>\n', 1))


def wirte_footer(f):
    f.write(indent('</LocalizedText>\n', 1))
    f.write('</GameData>\n')

def indent(string, indentation):
    indentation_string=''
    for i in range(indentation):
        indentation_string=indentation_string + '\t'
    return indentation_string + string

if __name__ == '__main__':
    get_data()
