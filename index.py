from helpers import fetch_reports
import os

if not os.path.exists('./reports'):
    os.mkdir('./reports')

for year in range(2000, 2020):
    if not os.path.exists('./reports/' + str(year)):
        os.makedirs('./reports/' + str(year))

    print('Fetching ' + str(year) + '...')

    try:
        reports = fetch_reports(year)

        for report in sorted(list(reports)):
            date = report.strftime("%d-%m-%Y")

            with open('./reports/' + str(year)
                      + '/' + date + '.txt', 'w') as file:
                file.write(reports[report])
    except Exception as e:
        print(e)
        continue

print('Finished!!!!')
