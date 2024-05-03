schema = {
  "address": {
          "type": "string",
          "description": "The address of the property."
    },
  "suiteNo":{
          "type": "integer",
          "description": "The suite number of the property. The suite number of the address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is 7. The property with address `2-4 Jackson Avenue, Sydney, NSW, 3000` does not have a suite number. The property may not have a street number. In this case, return None"
      },
    "streetNo":{
        "type": "string",
        "description": "The street number of the property. This is either a number like `2`, `45` etc or a range like `3-5` or `19-25` etc. The street number of the address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is 4. The suite number of the address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is 7. The property with address `2-4 Jackson Avenue, Sydney, NSW, 3000` has street number 2-4."
    },
    "streetName":{
        "type": "string",
        "description": "The street name of the property. The street name of the address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is `Spade Street`."
    },
    "City":{
        "type": "string",
        "description": "The city the property is in. The address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is  in `Port Douglas`."
    },
    "State":{
        "type": "string",
        "description": "The state the property is in. The address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is  in `QLD`. Possible values are one of `NSW, QLD, SA, WA, VIC, ACT, NT`. These are abbreviations respectively for New South Wales, Queensland, South Australia, Western Australia, Victoria, Australian Capital Territory and Northern Territories"
    },
    "PostCode":{
        "type": "integer",
        "description": "The postcode the property is in. The address `7 / 4 Spade Street PORT DOUGLAS QLD 4877 AUSTRALIA` is  in postcode `4877`."
    },
  "agentName1": {
  "type": "string",
  "description":"Enter the name of the primary listing agent if present in agent listing else NULL and do not make up the value"
  },
  "agentTel1": {
  "type":"string",
  "description":"Enter the phone number of the primary listing agent if present else NULL and do not make up the value"
  },
  "agentEmail1": {
  "type":"string",
  "description": "Enter the email of the primary listing agent if proper email present in the given text else NULL and do not make up the value "
  },
  
  "agentName2": {
  "type":"string",
  "description":"Enter the name of the secondary listing agent if present else NULL and do not make up the value"
  },
   "agentTel2": {
    "type":"string",
    "description":"Enter the phone number of the secondary listing agent if present else NULL and do not make up the value"
  },
  "agentEmail2":{
    "type":"string",
  "description": "Enter the email of the secondary listing agent if proper email present in the given text else NULL and do not make up the value "
  } ,
 
  "description": {
    "type":"string",
    "description":"Enter the description of the property as listed on the page. Be sure to list all features of the property, including amenities, facilities and features."
  },
  "buildingDetails": {
    "type":"string",
    "description":"Enter the details of the property, including area and the type of usage the property can be used for. Please be as detailed as possible."
  },
  "availableSpace":{
    "type":"string",
    "description": "Enter the available space in the property. This should be in square meters."
  },
  "spaceType":{
    "type":"string",
    "description":"Enter the usage types the property is suitable for as per the listing. For example, a property might be suitable for retail, offices and medical clinics. This will be listed explicitly on the page somewhere"
  },
  "listingUseType": {
    "type":"string",
    "description":"Enter the listing use types of the property. For example, a property might be suitable for retail, offices and medical clinics. This will be listed explicitly on the page somewhere"
  },
  "suiteStatus": {
    "type": "string",
    "description": "The status of the listing. This indicated whether the listing is active or closed. The values should be one of `Available, `Sold Out`, `Off the Market`, `Leased`, `Deleted` and `Lease Pending`"
  },
  "listingStatus": {
    "type": "string",
    "description": "The status of the listing. This indicated whether the listing is active or closed. The values should be one of `Available, `Sold Out`, `Off the Market`, `Leased`, `Deleted` and `Lease Pending`"
  },
  "outgoings":{
      "type" : "string" ,
      "description": "Enter the property price here and  also mention GST if applicable"
  }
}