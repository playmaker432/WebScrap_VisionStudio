# OCR Tool

## Description

This tool is used to extract text from images and output Chinese & English addresses. The purpose is to assist the daily work of business team by getting information in pictures. It uses the OCR (Azure AI Vision Audio) to perform the extraction by autiomation (Selenium).

## Preparation

1. Prepare the screenshots in the folder 'screenshots' (the folder is in the same folder as the application 'ko_screenshot.exe'). The screenshots should be in the format of '.png' or '.jpg'.

2. You may input any number of screenshots in the folders 'Greenshots_address' and 'contract'. But the output csv file will leave the part as null if the screenshot does not contain the complete information. (e.g. if you do not input any photos in the folder 'Greenshots_address', the output csv file will only contain the information of 'Contact', 'Telephone Number' and 'Page'.)

3. When catpuring the screenshots, please make sure that the screenshots are clear and the text is not covered by other objects. Also, the addresses should be shown as a whole in the screenshot. (e.g. if the address is shown in two lines in the screenshot, the output data will have problems)

## Pre-requisites

- There is no strict hardware requirements for this application.
- The application is developed and tested on Windows 10 Pro.

## HOW TO USE

1. Before tunning the application, please make sure that the screenshots are prepared. Please read the 'Preparation' section above.

2. The application will check the files in the pre-defined locations.If this is the first time to run the application, or the predefined directories has not been created, the application will automatically add following directories in 'C:\Users\{username}\Pictures\' with some demo pictures for testing:

   - ../Pictures/Greenshots_input

     - ../Pictures/Greenshots_input/Greenshots_address
     - ../Pictures/Greenshots_input/Greenshots_address

   - ../Pictures/Greenshots_output

3. Before running the application, please follow the instructions in the 'Preparation' section above. The system will also check the files in the pre-defined locations.

4. The application will run the OCR (Azure AI Vision Audio) in the website to perform the extraction by autiomation (Selenium). Please do not move the mouse cursor and input by keyboard before the browser is closed.

5. The application will save the output file in the same folder as the application and it will be opened after application is finished.

## Example Output

- The ouput file has 5 columns: 'Chinese Address','English Address', Contact, 'Telephone Number', 'Page'
- The output file will be saved as a csv file in the '../Pictures/Greenshots_output'
- The output file will be opened after application is finished.
- Please note that the Chinese result is not accurate. The result is only for reference and the user should check the result by themselves.

## Error Handling

- If you see any error, please refer to the instructions of this file and check the following points:

  - The screenshots are prepared in the right folders
  - The screenshots are in the format of '.png' or '.jpg'.
  - The screenshots are in the folder 'Greenshots_address' and 'Greenshots_contact'.

- Please do not move the mouse cursor and input by keyboard before the browser is closed.

- If you find any bugs, please contact the developer.

## OCR Website link

https://portal.vision.cognitive.azure.com/demo/extract-text-from-images"

https://getgreenshot.org
