
from bs4 import BeautifulSoup


def backtest_table_to_html(df, title, black_and_white=False):

    ## table columns to center, 
    ## everthing else is right justified
    COLUMNS_TO_CENTER = 'Date InDate ExDate InSignal ExSignal'.split()

    if black_and_white:
        HARD_COLOR = '#282A2D'
        SOFT_COLOR = '#5C5E5F'
    else:
        # Hannibal Blues...
        HARD_COLOR = '#0E2A52'
        SOFT_COLOR = '#315BA5'

    INDENT = '&nbsp;' * 2 

    # Convert the DataFrame to an HTML string with no border
    html_string = df.to_html(index=False, border=0)

    # Parse the HTML content
    soup = BeautifulSoup(html_string, 'html.parser')

    # Add the title above the table with the specified styles
    title_html = f'<div style="text-align: center; color: {HARD_COLOR}; font-family: Verdana;'
    title_html += f'font-size: 16pt; border: none; text-align: left;'
    title_html += f'margin-top: 20px; margin-bottom: 20px;">{INDENT}{title}</div>'
    title_soup = BeautifulSoup(title_html, 'html.parser')

    # Insert the styled title above the table and add a blank line (margin) for spacing
    soup.table.insert_before(title_soup)

    # Find the table header row and apply Helvetica font style, bold font weight, and padding
    header_row = soup.find('tr')
    if header_row:
        for th in header_row.find_all('th'):
            #th_style = 'font-family: Helvetica; font-size: 14pt; font-weight: bold; padding: 5px;'
            th_style = 'font-family: Verdana; font-size: 11pt; padding: 8px;'
            th_style += f'background-color: {HARD_COLOR}; color: white;'
            if th.text in COLUMNS_TO_CENTER:  
                th_style += 'text-align: center;'
            else:
                th_style += 'text-align: right;'
            th['style'] = th_style

    # Style all non-header rows
    rows = soup.find_all('tr')[1:]
    for index, row in enumerate(rows):
        # Apply general styles and specific styles for even rows
        for td in row.find_all('td'):
            #td_style = 'padding: 5px; font-family: Courier New; font-size: 14pt;'
            td_style = 'padding: 5px; font-family: Verdana; font-size: 12pt;'
            if index % 2 == 0:  # Style even rows differently
                td_style += f'background-color: {SOFT_COLOR}; color: white;'
            else:
                td_style += f'background-color: white; color: {HARD_COLOR};'
          
            for col_name in df.columns.tolist():
                if col_name in COLUMNS_TO_CENTER:
                    index_of_col = df.columns.get_loc(col_name)
                    if td.find_previous_siblings('td') is not None and len(td.find_previous_siblings('td')) == index_of_col:
                        td_style += ' text-align: center;'
                else:
                    td_style += ' text-align: right;'

            td['style'] = td_style 

    # Return modified HTML as a string
    return str(soup)


## test
if __name__ == '__main__':
    import pandas
    import random
    import datetime

    tbl = list()

    for i in range(1,16):
        dt = datetime.date(2010,10,i).strftime('%Y-%m-%d')
        jobs = ['Plumber', 'Racer', 'Stripper', 'Boxer', 'Driver', 'Sales', 'Cop', 'Fireman', 'Athlete', 'Doctor']
        job = random.choice(jobs)
        count = random.randint(20,90)

        m = dict(Date=dt, Count=count, ExSignal=job)
        tbl.append(m)

    df = pandas.DataFrame(tbl)
    new_html = backtest_table_to_html(df, 'Tester', True)
    print(new_html)

    with open('tester.html', 'w') as f:
        f.write(new_html + "\n")



