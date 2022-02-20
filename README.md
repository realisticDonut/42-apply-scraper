# ![42-apply-scraper](https://user-images.githubusercontent.com/86598034/154815974-415b9cdf-1444-4317-a186-e80c3c40f127.jpg)
42-Apply-Scraper
Automates the process of reading data from the 42 Apply Admin Platform using this webscraper.

## Description
The 42 Apply Admin platform does not offer a publicly usable API. This makes retrieving the data from the platform very tedious.
The downloadable .csv file offered by 42 Paris does not include all historical data, making statistical analysis a tricky and error-prone process.

This is why the 42-apply-scraper was created. This script logs in to the 42 Apply Admin platform and scrapes the correct numerical data from the corresponding pages. It is meant for the "Bocal", or staff, of a 42 campus.  
  
The data scraped is 100% anonymous, and only contains the number of applicants in certain steps/filters. No specific user data is read or saved.
Using the Google Drive Api and a Google Service account, the script then writes this data to a Google Sheets file.
This creates a very user-friendly and easily formattable data sheet that can be opened, interpreted, and used by practically anyone who knows how to use spreadsheets.

## Setup
### Prerequisites
Follow the following steps to set-up everything neccessary to use the webscraper:
#### 1. Docker
* *Linux (Debian based):*  
  Open up a Terminal and execute the following commands:
  ```
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io
  ```
* *MacOS/OS X:*  
  [Docker Installation Guide MacOS](https://docs.docker.com/desktop/mac/install/)

#### 2. Google Account  
A google account is neccessary to save the data to a Google Sheets file:
[Create Google Account](https://accounts.google.com/SignUp?hl=en)

#### 3. Google Service Account
Your google account needs an activated Google Service Account for the script to be able to connect to and use the Google Sheets Api:
1. [Google Service Account Guide](https://support.google.com/a/answer/7378726?hl=en)  
```
Make sure you activate the Google Drive API in step 2 of the guide.
```
2. Place the downloaded .json file (Google Service Account credentials key) in the "/Scraper/" directory within the project folder.

#### 4. Google Sheets Template
Upload the "Apply Data.xlsx" file into your Google Account:
1. Go to https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts?supportedpurview=project
2. Choose your newly created project.
3. Copy the email address of your service account.
4. Download the "Apply Data.xlsx" file from the repository
5. Go to [Google Sheets](https://docs.google.com/spreadsheets/u/0/?tgif=d)
6. Click on "Blank" under "Start a new spreadsheet"
7. Click on "File" -> "Open" -> "Upload" -> choose the "Apply Data.xlsx" file downloaded in step 4.
8. Within this spreadsheet, click on the "Share" Button on the top right hand corner.
9. Add the copied email address from step 3.
10. Set-Up the Template to fit your scraping needs: [Google Sheets file formatting](#google-sheets-file-formatting)

### Installation
1. Open up a terminal
2. Navigate to a directory you would like to install the 42-apply-scraper in:
  *Linux (Debian based):* and MacOS:
  ```
  cd "pathtodirectory"
  ```
3. Clone the repository:
  ```
  git clone git@github.com:realisticDonut/42-apply-scraper.git
  ```
4. Navigate into cloned directory:
  ```
  cd 42-apply-scraper
  ```
5. [Set-up your config file](#config-file-set-up)
6. [Format your Google Sheets file](#google-sheets-file-formatting)
7. Build Docker image
  ```
  docker build -t 42-apply-scraper .
  ```

## Running the script

### Run
Execute the following command in the terminal:
  ```
  docker run 42-apply-scraper
  ```
The script will then Initialize the scraper, log in to the Google Service Account, log in to the Apply Admin Platform, scrape the data from the pages, and  write them to the Google Sheets file automatically. This can take up to 2 minutes.

### Automate
Use any scheduling tool (like cron) to automatically run the script at certain time intervalls.
Have the scheduler simply run:
  ```
  docker run 42-apply-scraper
  ```
when needed.


## Config file set up
The config.py file is used to change the settings of the script and needs to be set-up correctly.  
**IMPORTANT:** This file contains your Apply Admin Credentials. Make sure you restrict access rights to the file and system.

Fill out all fields in this file by writing the required information within the quotes ''
1. sheet_name = '' *The name of the Google Sheets file uploaded during [prerequisites](#prerequisites)*  
![image](https://user-images.githubusercontent.com/86598034/154822621-cbe763da-40a8-4c19-b9b1-2bff47b8fe3f.png)

2. sheet_data = '' *The name of the spreadsheet the data will be saved into (Part of the Google sheets file in step 1)*  
<img width="130" alt="image" src="https://user-images.githubusercontent.com/86598034/154822643-469be697-9267-40a8-9530-76528e182e93.png">

3. path_google_cred = '' *file name of the downloaded json file while creating your google service account*
4. link_admin_login = '' *full URL of the 42 Apply admin page of your campus. Example 42 Heilbronn: https://apply.42heilbronn.de/users/auth/marvin*
5. username = '' *user name of your Apply Admin Account*
6. password = '' *password of your apply Admin Account*

## Google Sheets file formatting
The google sheets file can be formatted very freely.
The following rules apply:
1. A cell containing "Data Link ⇨" must exist in any cell in the "A" column. The entire row where this cell is located in is reserved for a column's data link.  
   The scraper iterates through all columns' data link, scrapes the corresponding data from the 42 Apply Platform, and writes it underneath this link in the next    free row.  
   A column's data link cell can contain the following values:  
   * **Empty:** The column will be skipped, no data will be written into the next free cell. Use this if you would like to add relative data or Formulas to a cell      (example: A1=B1-C1)
   * **Any Numerical Value:** This value will always be written into the next free cell
   * **42 Apply Platform Data Link:** A link to a search-result page on the 42 Apply admin platform.
     To create such a link:
     1. Go to https://apply.42heilbronn.de/admin and click on "APPLICANTS".  
     2. Add filters to the search field that represent the data you would like to have scraped:<img width="200" alt="Screen Shot 2022-02-20 at 1 02 56 AM" src="https://user-images.githubusercontent.com/86598034/154823274-747f1c92-0485-4bea-b0b7-5250e9000203.png">
     3. Click on "SEARCH". The URL of this page is your data link.
     4. The number of results on this page (= number of applicants within this filter) will be written into the next free row in the same column as this link.
2. The date of each execution will be automatically written into the first column of a row.
3. As long as these rules are respected, you are free to add, remove, change, and re-format cells as you wish.

### Example: 
 <img width="951" alt="Screen Shot 2022-02-20 at 1 29 36 AM" src="https://user-images.githubusercontent.com/86598034/154823788-6ef96099-3e6f-4508-8883-3b16349de834.png">

```
Freely formatted cells (Green Box): Can be formatted, renamed, removed, added, etc. as you wish.
```

```
Data link row (Red Box): Must exist! First Cell within this row must be called "Data Link ⇨". All data from these links will be written in the same column in the next free row underneath the cell.
```

```
Automatically scraped data rows (Blue Box): These rows are filled out automatically when running the script, including the date.
```

```
Because the "Data link" of the first column is a URL of a search result, the scraper will retrieve the data from this link and write it in der next free row underneath.

Because the "Data link" of the second column is empty, all cells underneath will stay untouched.

Because the "Data link" of the third column is a numerical value, all cells underneath will be overwritten with this number.
```


## Future Plans / TODOs
* Implement a more secure way of saving login credentials
* Add the ability to save scraped data as a CSV file

## Contact
Please contact agebert42@gmail.com for information or bug-reports.
Feel free to optimize the code :)
