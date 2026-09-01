---
title: "Customize Service Manager Business Services CI for Relationship with Cireson Asset Management Organizations"
date: 2015-04-09T23:34:46Z
draft: false
slug: "customize-service-manager-business-services-ci-for-relationship-with-cireson-asset-management-organizations"
tags:
  - "Cireson"
categories:
  - "Service Manager"
---

I had a request where the question was if it was possible to customize the Business Services Configuration Items in Service Manager, so that it could reference Organizations defined in Asset Management CMDB. In this case, the Asset Management solution in Service Manager was based on Cireson Asset Management, but the following solution could easily be applied for other Asset Management solutions as well.
If you look at the built-in Configuration Items and Business Services in Service Manager, you will see that there already is a field for "Owned By Organization". This built-in field however is based on a simple string value:
![](/uploads/2015/04/040915_2328_customizese1.png)
The question was to replace this field with a single instance picker, which would reference the Organizations defined in Cireson Asset Management:
![](/uploads/2015/04/040915_2328_customizese2.png)

## The solution

The solution consists of several parts, which I will explain in this blog post:

- A sealed Management Pack which consists of the required class extension for referencing Cireson Asset Management.
- An unsealed Management Pack for Type Projection and Form Customization, so that the Business Service Form can show the single instance picker for the custom relationship.

Optionally, you could create a custom form in Visual Studio instead, but then you would have to create all the other fields for Business Service as well.

## The first part, "extending" the Service class

So first, I would have to create a new Management Pack for the class extension. To do this I use the Service Manager Authoring Tool, and create a new blank Management Pack xml file.
I want to extend the Business Service class, and after examining Service Manager and classes, I found these relationships between the relevant classes for my scenario:
![](/uploads/2015/04/040915_2328_customizese3.png)
The "Service" and "User Created Distributed Application" classes are abstract classes. These classes cannot contain instances, and acts as base classes for inherited classes. Therefore, normally this means that the class I would want to extend is the "Business Service" class.
But! There is a caveat here. There are two types of Services in the Service Manager CMDB: Those that you manually create and those you would synchronize from Operations Manager as Distributed Applications. If I were to extend the Business Service class this would only be available for my manually created Business Services, and besides that I will have a problem with the default view and default form in Service Manager Console as it targets the Service class. Trust me, I have been there ;)
This challenge is well described in Oskar Landman's blog post: <http://www.authoringfriday.com/2013/04/27/scsmscom-business-service-extension/>.
So I decided to base my solution on the workarounds described in that article, with a little tweaks and customizations.
Using Service Manager Authoring Tool I create a new Configuration Item Class and name it with an appropriate internal name.
![](/uploads/2015/04/040915_2328_customizese4.png)
I delete the default ID Property\_4, ignore the warnings, and create my own ID property with auto increment, default value and key configured as:
![](/uploads/2015/04/040915_2328_customizese5.png)
I then create a relationship choosing the target to the Service class, and specifying source max cardinality to 1:
![](/uploads/2015/04/040915_2328_customizese6.png)
Next, to prepare for creating the relationship to the Cireson Asset Management, I find and import the sealed CiresonAssetManagement.mp file to the Authoring Tool. This file can be downloaded with the AssetManagement.zip from Cireson and can be located in the Authoring folder in the zip file.
From my custom class for Business Service, I then click on the Create Relationship button and give it an internal ID and name. I then choose Target Class and browse to the Cireson Asset Management Pack and selecting Organization:
![](/uploads/2015/04/040915_2328_customizese7.png)
I save my Management Pack file and then choose to close the Solution in Service Manager Authoring Tool. I will now edit and clean up the XML file manually, which I always find is good practice.
Tip: When I save XML MP files in Service Manager Authoring Tool, and later open the files in Notepad I always get the word wrapping all messed up. I usually open the file in XML Notepad 2007 (yes, I know, but it works;), save it, and then I can open it in Notepad again. Then the XML file is formatted nicely and line by line. You can also work with the xml file in Notepad++.
So if you have been following me until now, you might have a MP XML with Type Definitions that looks like this (don't mind the my custom names for aliases, you might have Guids there instead):
[![](/uploads/2015/04/040915_2328_customizese8.png)](/uploads/2015/04/040915_2328_customizese8.png)
My custom class for extending Service are now finished, I just need to seal the XML file to a MP file. In Service Manager Authoring Tool I open the xml file again, and then sealing it. I have already prepared a Strong Name Key file (.snk) to use when sealing my custom Management Packs.
That concludes the first part, and I can now import this sealed MP to Service Manager. In the next part I need to work on the forms and type projections.

## Second part, type projection and form customization

At this point, I have a working relationship between the custom class for Business Service and the Service class and Organizations in Cireson Asset Management. It is just that I do not have any forms or views to see or edit them! Therefore, this second part will focus on creating the required type projections and form customizations so that I can see and edit those relationships.
In Service Manager Authoring Tool, I close any open solutions, and then open the sealed MP from part one. I also create a new blank Management Pack XML to contain my form customizations.

### Create a blank form for the custom class

I then create a new Form, specifying the Business Service Custom Class as my Base class:
[![](/uploads/2015/04/040915_2328_customizese9.png)](/uploads/2015/04/040915_2328_customizese9.png)
I then create a simple form. I create labels and textboxes for my custom ID and Display Name, and single instance picker for the related Service and Organization. For each of these I change the binding path, for example:
![](/uploads/2015/04/040915_2328_customizese10.png)
I now have a custom form that I can use for creating new instances of the custom class of Business Services, but need to customize the default main form for Service to be able work with my custom relationship there.

### Customizing Service main form and type projections

From the Form Browser I find the ServiceMainForm, and click to View it. When right clicking this form I select to Customize it. I'm prompted to choose my unsealed XML Management Pack file and the form will open as customizable.
I can now easily see the text box for Owned By Organization. I select it and from Properties I set the Visibility to Hidden. (I could have deleted it but prefer to have the text box in the Management Pack if I should want it back).
From the Form Customization Toolbox, drag the Single Instance Picker over the place where the Owned By Organization textbox was. Do not change any bindings yet. This should now look something like this:
![](/uploads/2015/04/040915_2328_customizese11.png)
At this point, I have to step out of the Service Manager Authoring Tool, and do some XML editing. I save and close the unsealed Management Pack in the Management Pack Explorer, and open the XML file in my text editor.
After renaming some aliases and ID's to be more readable, I can look over my existing Type Projections. I have two Type Projections, the first one for the blank form I created, and the second one for the customized default Service form:
[![](/uploads/2015/04/040915_2328_customizese12.png)](/uploads/2015/04/040915_2328_customizese12.png)
Further down in the XML file I can see the two Forms, targeting each of the above Type Projections (I have collapsed the Customization part to make it more readable):
[![](/uploads/2015/04/040915_2328_customizese13.png)](/uploads/2015/04/040915_2328_customizese13.png)
I now need to add to the Type Projection for the customized Service Form, so that the relationship that I created earlier can be used. This is done by adding the following two components, specifying SeedRole='Target' for the relationship for the custom Service class and inside that a component for the Asset Organization relationship:
[![](/uploads/2015/04/040915_2328_customizese14.png)](/uploads/2015/04/040915_2328_customizese14.png)
I can now save and open this XML file again in Service Manager Authoring Tool, and go to the single instance picker I added for the customized Service Form earlier and change the Binding and Instance type. I set the Instance type to Organization from Cireson Asset Management, and the Binding Path manually to "*CustomBusinessService\_Relationship\_Service***.***CustomBusinessService\_Relationship\_AssetOrganization"*. This has to be entered manually and cannot be browsed, and the binding path will traverse the two relationships specified in the added component paths from above.
[![](/uploads/2015/04/040915_2328_customizese15.png)](/uploads/2015/04/040915_2328_customizese15.png)
I have now completed the form customizations and type projections, and can import this Management Pack to Service Manager. I do not have to seal it, as it refers to the other Management Pack for the custom class that was sealed.
As a last step, I need to create a view for the custom Service class.

### Creating a view for the custom Service class

In Service Manager Console I can now create a view under Configuration Items targeting the Custom Service Class. This will let me create instances of the custom class for Business Services and relate them to the Business Services I have either created manually or synchronized from Operations Manager.
In this example I have a Business Service for Self Service Portal, and create a relationship to it:
![](/uploads/2015/04/040915_2328_customizese16.png)
I can now open the Business Service form, and use the instance picker for selection the Organizations I have added to the Asset Management:
![](/uploads/2015/04/040915_2328_customizese17.png)
That concludes this blog post, hope it has been helpful!
