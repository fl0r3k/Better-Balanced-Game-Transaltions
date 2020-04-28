import pandas as pd

langs = ['en_US', 'fr_FR', 'pl_PL', 'ru_RU', 'ko_KR']


def generate_completness_report():
    xlsx = pd.ExcelFile('translations.xlsx')
    metadata_frame = pd.read_excel(xlsx, 'metadata')
    metadata_frame.sort_values(inplace=True, by=['Tag'])

    print('====================')
    print('===== metadata =====')
    print('====================')

    nunique = metadata_frame.Tag.nunique()
    dtags = metadata_frame[metadata_frame.Tag.duplicated()].Tag
    nduplicated = len(dtags)

    print('Number of unique TAGs: ' + str(nunique))
    print('Number of duplicated TAGs: ' + str(nduplicated))
    if nduplicated > 0:
        print('Duplicated TAGs:')
        for t in dtags:
            print(t)

    print('\n\n')

    for lang in langs:
        print('=================')
        print('===== ' + lang + ' =====')
        print('=================')
        lang_frame = pd.read_excel(xlsx, lang, index_col=0)

        merged = pd.merge(metadata_frame, lang_frame, how='outer', on='Tag', indicator=True)


        # lang tags missing
        ltags = merged[merged._merge.eq('left_only')].Tag
        print('\n' + str(len(ltags)) + ' TAGs missing in lang\n')
        for i in ltags:
            print(i)

        # metadata tags missing
        mtags = merged[merged._merge.eq('right_only')].Tag
        print('\n' + str(len(mtags)) + ' TAGs missing in metadata\n')
        for i in mtags:
            print(i)

        print('\n\n')

if __name__ == '__main__':
    generate_completness_report()
