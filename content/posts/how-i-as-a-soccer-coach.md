---
title: "How I as a Soccer Coach...."
date: 2020-04-08T20:14:26Z
draft: false
slug: "how-i-as-a-soccer-coach"
tags:
  - "Forms"
categories:
  - "Microsoft Flow"
  - "Microsoft Forms"
  - "Microsoft Teams"
  - "Power Automate"
---

## .....moved trainings and meetings online using the modern collaboration tools I know and love!



When I'm not working or fulfilling my community activities as MVP, I spend many evenings and weekends at the soccer field, where I'm coaching and managing a soccer team consisting of 14 year old boys.



Due to the Coronavirus situation, as in many countries also Norway has closed it schools, many businesses are either closed or working from home, and in general we are all following the rules of isolating to make sure the virus doesn't spread. And of course, this has also resulted in closing all grass roots football, for the time being at least to the end of April. I quickly understood that I needed to think in new ways..


> So I decided to use the tools I have at hand, and I created virtual follow ups using tools like Microsoft Teams, Forms, Power Automate and SharePoint Online among a few to help support the boys doing self practice and have Virtual team Meetings..



This blog post is a technical version of a LinkedIn article I wrote in Norwegian, <https://www.linkedin.com/pulse/hvordan-jeg-som-fotballtrener-jan-vidar-elven/>, explaining more the reasons and why I set this up. In this post I will go more into the technical setup, and share some resources for those that want to learn or maybe do something similar themselves. Some of the screenshot images are in Norwegian, but you should be able to understand from my comments.



### It all started with Microsoft Teams.. and a Form!



I knew already from before that Microsoft Teams would be more central in my daily work, but I also observed that my son and his classmates, that also plays on the aforementioned soccer team, use Teams themselves now for digital schooling at home. They have daily Teams meetings, as well as some online classes and homework delivery.



So I thought that I wanted to set up a player meeting on Teams, and later a meeting with their parents. This way we could have a social and digital arena to meet each other, as well as talk with the boys how we wanted them to do training with self practice at home. So the first thing was to invite to online meetings.


![](/uploads/2020/04/linkedinspillermc3b8teonline.png?w=1024)



I knew that the boys already used Teams in school, but I needed to collect their school e-mail addresses. I also suspected several of the parents use Teams at their workplace, but not everyone, so I also needed to get an overview on that. So I decided to create a questionnaire in Microsoft Forms:


![](/uploads/2020/04/linkedinformsteams.png?w=752)



#### How I set it up:



I created a Form with the following inputs:



- Name (Text). The person filling in the form.
- Using Teams from before? (Choice). Yes, No and Don't Know option for parents to answer if they use Teams already.
- Parents, Teams e-mail address (Text). Their existing Teams work e-mail address or personal e-mail address.
- Players, Teams e-mail address (Text). The Teams e-mail address they use at school.



In addition I used the club logo and customized the theme colors for the Form. Then I selected Share settings and selected so that "Anyone with the link can respond". This will mean that all responses are anonymous, so that's why I require that they type their name in the first input. Then I distributed the Forms link to the parents.



After I received all the responses, I created a Teams meeting invite to the players for the players online meeting, and a Teams meeting invite to the parents for the parents online meeting.



We were now ready for our inaugural online meetings!



### Organizing Self Practice Trainings



Normally our soccer team practice at least 3 times a week, in addition to playing games or other activities. So before we had the online player meeting, a self practice training plan was created, focusing on 3 weekly trainings:



- Conditioning (interval runs, with or without ball, dribbles, jumps and obstacles etc.)
- Technique, Agility and Strength (ball possession, passing, runs, sprints, physical strength)
- Endurance (long hikes and outdoor activity with family)



These training should be completed after plan where the boys will get approved attendance for each training they complete. To get a training approved they needed to self register a training form, as well as document by sharing pictures, video, screenshots of activity etc.



The players were shown examples of activities and drills they could complete themselves or with help of family. With this organization and training plan, the only thing that was missing was a system for registering self practice and how I could follow up on that.



I decided to create another Form. In this Form which the boys got a shared link to, they could register their name, date, self assessment, what kind of activity they did and type, provide a description and optionally register number of minutes and kilometres. They were also asked to send in documentation with video, pictures, etc.


![](/uploads/2020/04/linkedinformsegentrening.png?w=674)



This worked really great and next week we already had a lot of responses for completed trainings:


![](/uploads/2020/04/linkedinformsresponses.png?w=768)



And from the media I received I could really see that the boys were doing their self practice:


![](/uploads/2020/04/2020-04-01_15-00-15.jpg?w=800)



#### How I set it up:



I created a Form with the following inputs:



- Name (Text). The player name filling in the form.
- Activity Type (Choice). Conditioning, Technique + Strength, or Endurance.
- Date of Activity (Date).
- Self Assessment (Rating). 1-5 stars where they could evaluate their own session.
- Type of Condition (Choice). If they did conditioning work, what kind of interval (4x4, 60x60, 15x15).
- Technique + Strength (Text, Long). Comment field for explaining how they did technique and strength work.
- Endurance (Text, Long). Comment field for explaining what kind of long activity they did.
- Number of Kilometres (Text, Restricted to Number). Optionally how many kilometres they practiced.
- Number of Minutes (Text, Restricted to Number). Optionally how many minutes the activity lasted.
- Sent media of activity (Choice). Yes or No for if they have sent picture, video or screenshot to our team e-mail address.



Also in this Form I used the club logo and customized the theme colors. Then I selected Share settings and selected so that "Anyone with the link can respond".



PS! I was looking into a File Upload response in the Form, but this cannot be added to a Form that are shared externally. That is why I needed the boys, or their parents, to send their media files to our e-mail address in addition to the Form registration.



### Following up on Registered Self Practice Trainings



With all those great responses coming in, I could look through the responses in Office Forms, and download an Excel copy of the responses, but I needed something more to follow up the trainings. So I created a private Team in Microsoft Teams:


![](/uploads/2020/04/linkedinegentreningsteam.png?w=610)



Next I wanted to get all the responses from Forms into a SharePoint List. I created the List into the Teams SharePoint Site so that I could get all the registered self practice trainings in one place, and be able to do edits if needed. I also added some extra columns for approve the training and if there was sent media documentation:


![](/uploads/2020/04/linkedinegentreningssplist.png?w=1024)


> Now the only thing I needed was some kind of automation that could bring every response from Forms over to this list: Enter Power Automate!



With the help of Power Automate I created the following Flow to automate that every time a new response is submitted in the Form, this would trigger the Flow:


![](/uploads/2020/04/linkedinflow1.png?w=669)



Next I needed to do some magic on the number inputs, I'll get back to that in the "How I did it:" section, but the Flow then created a new SharePoint List Item:


![](/uploads/2020/04/linkedinflow3.png?w=637)



#### How I did it:



The first thing I did was to create the Team that would also host the SharePoint Online Site for my list. The Team was created in my own tenant as a private team, and I elected not to invite any player, or parent, to the Team as guests at this point.



The SharePoint list was created with the following columns to reflect the Form:



- Renamed Title column to Name
- Type of Activity (Choice, with the same values as from the Form)
- Date (Date and Time, Include Time: No)
- Self Assessment (Number)
- Type of Fitness/Conditioning Activity (Choice, with same values as from the Form)
- Technique + Strenght (Multiple Lines of Text)
- Endurance/Long Actitivty (Multiple Lines of Text)
- Sent Picture (Yes/No)
- Number of Km (Number)
- Number of Mins (Number)
- Approved (Yes/No)
- Submitted (Date and Time, Include Time: Yes)



After the list with all the columns was created, the next step was to create the Flow in Power Automate. You can create Flows directly from the SharePoint List, as shown below, and then use one of the provided templates:


![](/uploads/2020/04/flowcreate.png?w=490)



Myself I started at https://flow.microsoft.com and selected to create a new Flow as Automated - from blank, and the selecting the trigger for "When a new response is submitted":


![](/uploads/2020/04/flowcreate2.png?w=450)


![](/uploads/2020/04/flowcreate3.png?w=869)



After I give a name to the Flow and select which Form I want to trigger on responses from, I add an Action to get the response details, as shown below:


![](/uploads/2020/04/linkedinflow1-1.png?w=669)



The next part is a little more complex. When a Form response is submitted, all response details will be provided as Strings. And if I try to update those values directly into the SharePoint list, it will fail because the Column require a number format. So I need to convert those string values to either Integer or Float respectively.



Power Automate have some Data Operation Actions I can use in Flows, and I have used the following three Compose actions, where I get the Self Assessment, Number of Km and Number of Min response details:


![](/uploads/2020/04/image.png?w=617)



The Compose action will create objects I can refer back to later in the Flow. The next complex thing is that I need to check if there are any values for number of kilometers and minutes, and these Form fields are not required and can be empty. There could be several ways to do this, I did it this way:


![](/uploads/2020/04/image-1.png?w=1024)



As shown above, I first add an Action for Initialize Variable, and give it the name for AntallKm (Number of Km), and set the initial value to 0. I specify that the type is Float (as I want to have decimal values). Next I add a Condition action, where I check if the ComposeAntallKm is empty, meaning it is equal to false. I do this as an expression, where the expression is using the empty function and checking against the output from the ComposeAntallKM earlier: empty(outputs('ComposeAntallKm'))


![](/uploads/2020/04/image-2.png?w=635)



If this condition evaluates to false, meaning that there has been provided a value in the Form, then the Flow will go to the If Yes action, and I convert the string to a Float value with the expression: float(outputs('ComposeAntallKm')), I've tried to illustrate that with the green arrow below. This expression would have failed the Flow if I didn't check if it was empty or not. If the value is empty, it would go to the If No action, and this is just empty because I then just let the value be the default 0 i provided when I initialized the variable (illustrated with the red arrow below).


![](/uploads/2020/04/image-3.png?w=1024)



Next in the Flow, I do the exact same logic for the number of minutes:


![](/uploads/2020/04/image-4.png?w=1024)



I'm now ready to update the SharePoint List with a new item. I select the SharePoint Online Create item action, and after specifying the Site and List name, I'll choose most of the item values from the dynamic content picker. The Km and Minutes values are picked from the respective variable. And for Self Assessment, I do this with an expression consisting of the int function that converts the string to an integer from the Compose action further up.


![](/uploads/2020/04/image-5.png?w=990)



For reference, my entire Flow at this point is shown below (collapsed without action details):


![](/uploads/2020/04/image-6.png?w=623)



### Take it to the Next Level - Teams Bot with Adaptive Card!



At this point I have a working solution where I get all new responses put in to the SharePoint List. I can now look through, edit and approve the registered trainings.



An even cooler solution would be that each registered training will be posted to the Team Channel as an adaptive card, where I can edit and approve and submit that back so that the list would be updated directly. That way I can follow up and check trainings in my Teams client on either my PC or Mobile, without needing to go to the SharePoint list.



So I added a couple of more steps to my Flow after the Create item action. First I added an action for posting an Adaptive Card to a Teams Channel and wait for a response, the next step was to Update the list item with the values.


![](/uploads/2020/04/image-7.png?w=626)



I will go into more details later under the "How I did it" section, but the end result of this was that every time a player submits a new training activity, I will get this Adaptive Card in my Teams Channel, summarizing the details of the training and providing me with the ability to edit the player name in case they typed it wrong, update any values for km or minutes, and select yes or no for if the player has sent photos or the training is approved:


![](/uploads/2020/04/linkedinadaptivecardtinius.png?w=575)



When I click the Update button, the values are submitted back to the Flow and the List item is updated.



#### How I did it:



Before I go into the Flow details on how to post adaptive card to Teams channel and process the response back, I want to show how I built the adaptive card.



Adaptive cards are posted as a JSON formatted message. You can read more about it here [https://](https://adaptivecards.io/)[adaptivecards.io](https://adaptivecards.io/)[/](https://adaptivecards.io/), see samples and usage scenarios and more. There's also a great resource called the Adaptive Cards Designer, <https://adaptivecards.io/designer/>, where you can build your own cards from blank or using one of the sample templates.



The designer lets you add controls and configure properties visually, while producing the JSON message you will need later. This is the design format of the card I ended up with, a little bit of Norwegian text here but you get the main idea, note that I have some placeholder values her, from where I will add data from my Flow later:


![](/uploads/2020/04/linkedinadaptivecarddesigner.png?w=991)



In the "Card Payload Editor" window you will see the JSON format you will need use in your Flow, and in the following snippet I'll provide you with my JSON message for this example here for you to reuse or build on as you like:



```json
{
    "type": "AdaptiveCard",
    "version": "1.0",
    "body": [
        {
            "type": "Image",
            "altText": "Borgen IL",
            "url": "https://borgensawebstorage.z6.web.core.windows.net/borgen_logo.png"
        },
        {
            "type": "TextBlock",
            "size": "Large",
            "weight": "Bolder",
            "id": "Title",
            "text": "Ny Egentrening Registrert!",
            "horizontalAlignment": "Left"
        },
        {
            "type": "TextBlock",
            "text": "Ny egentrening er registrert av <NAVN>.",
            "wrap": true
        },
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "Type Treningsøkt",
                    "value": ""
                },
                {
                    "title": "Dato",
                    "value": ""
                },
                {
                    "title": "Egenvurdering",
                    "value": ""
                },
                {
                    "title": "Økt beskrivelse",
                    "value": ""
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "Verifisering",
            "size": "Large",
            "weight": "Bolder",
            "color": "Attention"
        },
        {
            "type": "TextBlock",
            "text": "Verifiser treningsdata og eventuelt oppdater:",
            "size": "Small",
            "weight": "Bolder"
        },
        {
            "type": "TextBlock",
            "text": "Spillernavn",
            "size": "Medium",
            "weight": "Bolder",
            "color": "Attention"
        },
        {
            "type": "Input.Text",
            "value": "",
            "style": "text",
            "isMultiline": false,
            "maxLength": 50,
            "id": "Spillernavn_input"
        },
        {
            "type": "TextBlock",
            "text": "Antall Km",
            "size": "Medium",
            "weight": "Bolder",
            "color": "Attention"
        },
        {
            "type": "Input.Number",
            "value": "",
            "style": "text",
            "isMultiline": false,
            "maxLength": 20,
            "id": "AntallKm_input"
        },
        {
            "type": "TextBlock",
            "text": "Antall Minutter",
            "size": "Medium",
            "weight": "Bolder",
            "color": "Attention"
        },
        {
            "type": "Input.Number",
            "value": "",
            "style": "text",
            "isMultiline": false,
            "maxLength": 20,
            "id": "AntallMin_input"
        },
        {
            "type": "TextBlock",
            "size": "Large",
            "weight": "Bolder",
            "color": "Attention",
            "text": "Godkjenn",
            "horizontalAlignment": "Left"
        },
        {
            "type": "TextBlock",
            "size": "Small",
            "weight": "Bolder",
            "text": "Har spilleren sendt skjermbilde, bilde eller video?",
            "horizontalAlignment": "Left",
            "separator": true
        },
        {
            "type": "Input.ChoiceSet",
            "id": "input_media",
            "value": "1",
            "choices": [
                {
                    "title": "Nei",
                    "value": "false"
                },
                {
                    "title": "Ja",
                    "value": "true"
                }
            ],
            "style": "expanded"
        },
        {
            "type": "TextBlock",
            "size": "Small",
            "weight": "Bolder",
            "text": "Er egentreningen godkjent?",
            "horizontalAlignment": "Left",
            "separator": true
        },
        {
            "type": "Input.ChoiceSet",
            "id": "input_godkjent",
            "value": "1",
            "choices": [
                {
                    "title": "Nei",
                    "value": "false"
                },
                {
                    "title": "Ja",
                    "value": "true"
                }
            ],
            "style": "expanded"
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Oppdater"
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
}
```



With that JSON message ready, I can now add the "Post an Adaptive Card to a Teams Channel and wait for a response" action to my Flow. I select my Team, and the Channel I want to post the adaptive card to, and then paste in the JSON message from the Adaptive Card Designer:


![](/uploads/2020/04/linkedinflow4.png?w=619)


![](/uploads/2020/04/image-8.png?w=559)



![](/uploads/2020/04/image-10.png?w=612)


![](/uploads/2020/04/image-11.png?w=500)



As you can see from the images above, I've added dynamic data from the Flow where I had placeholders for values. Note also that I use the values "false" and "true" for the Input.ChoiceSet, this will make it correct when I set the values back to the updated List item.



PS! Another important thing to note is the "id" property of the inputs I want to be able to update back to the Flow. This "id" property needs to be specified later.



The Update message is what will be shown back in Teams after the Adaptive Card has been updated and submitted back with the Action.Submit button. It will look like this:


![](/uploads/2020/04/image-12.png?w=553)



After the card is updated, a response will be sent back to the Flow. So my next step would be to add a Update item action for updating the selected values in the SharePoint List. From here I will select the SharePoint Site and List Name, and then getting the Id for the existing list item I want to update. This Id is from the earlier action in the Flow from where I created the list item:


![](/uploads/2020/04/image-13.png?w=611)



The values I want to update back in the List from the Adaptive Card Response is shown above with the blue Teams icon. I will have to specify these by adding an expression that looks like the following, as there are currently no dynamic output from the previous action I can select:



```text
outputs('Post_Adaptive_Card_to_Egentrening_Teams_Channel_Wait_Response')?['body/data/Spillernavn_input']
```



Note the following from above, refers back to the action name (since I had blank spaces in the step name, I will have to refer back to it with underscore), and from the response body and data section I will refer to the "id" property of the adaptive card input.



Create similar expressions for the other inputs, and that should be it! The complete Flow step is now like this:


![](/uploads/2020/04/image-15.png?w=611)



### Summary and Next Steps



In this quite lengthy blog post I have shown how I built myself a great follow up solution for my soccer team self practice trainings. The boys find it easy to use, and I can use the tools and solutions I know and love for following up. I have also learnt quite a bit of new tricks and tips ;)



I also start to have some great statistics, I can summarize and rank the players so that I can create a top 10 list for example. And these ranks can be published to the boys, they do love a competition and this can motivate them to do some extra work. I have created this HTML table, that I update semi-manually now. I'm already working in the next Flow that will publish updates to this table automatically. So there might be a follow up blog post on this.. ;)


![](/uploads/2020/04/linkedinleaderbord.png?w=1024)



I hope this has been helpful or/and inspiring, reach out to me if you have questions, and remember the Power of the Flow :)
