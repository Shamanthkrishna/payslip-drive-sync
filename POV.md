So my pay slips are present in a portal called Paybooks, where I login and i can see my payslips after naviugating a little and download them, now i need an automation for this so that every month its downlaoded and stored in a specific folder of my google drive
How cna I do this automation, what are the dependencises, im planning to do it using python hence tlel me what can be done so that automatically its triggered and thje file is stroed everymonth


Login URL:https://ess.paybooks.in/
Credentials:
Login ID: 1240901
Password: skb2025@paybook
Domain: TISMO

In the home page itself there's a button for previous month pay slip if we click on that, a brief detailed pay slip is displayed where another button is present for downloading so upon clicking it the pay slip gets downlaoded, this downloaded payslip must be uplaoded to a specific drive folder of my personal drive, there's an option to mail the payslip but that will mail it to my work email id.
So anytime on the 1st week of the month, the previous m onths pay slip is taken and put into my drive this is my idea, even while uplaoding it to drive it should properly prganised by creating a folder for the previous month and uplaoding isnide it. 


Google drive folder path will be something like this:
/Pay Slips/2025/December/December_2025_PaySlip.pdf
Ill give you the exact path once development is started.

Downloaded filename doesnt matter let it be anyway but if the month name is added, that would be better for naming skae and reading sake

Check if the file exists 1st, if not then add or else skip

If any error comes then notify through mail
Also Logging is required, saving the log file will bhe discussed later

Im not sure about the execution method, where will it be hosted etc,
Ig since its my present working company payslips so if i login to my office pc then once in a month the service will trigger and save it to my drive, log file will be in my local pc
Since i have no intention to pay and use some cloud jus to host this application henc euse my local office pc anyway i daily logina nd work in the same pc, so once in a month it will trigger automatically and then do the business, isnt that fine?
