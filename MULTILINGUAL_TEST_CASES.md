# ULAVI VOCIS Multilingual Test Cases

## India Tamil

Input:
`Enakku naalaikku kaalai 10 manikku Chennai Airport irundhu Villivakkam poganum.`

Expected:
```json
{
  "serviceType": "Airport Transfer",
  "pickup": "Chennai Airport",
  "dropoff": "Villivakkam",
  "date": "Tomorrow",
  "time": "10:00 AM"
}
```

## India Hindi

Input:
`Mujhe kal subah 9 baje Delhi Airport se Noida jana hai.`

Expected:
```json
{
  "pickup": "Delhi Airport",
  "dropoff": "Noida",
  "time": "09:00 AM"
}
```

## Singapore English

Input:
`Pick me up from Changi Airport and drop me at Marina Bay Sands tomorrow at 8 PM.`

Expected:
```json
{
  "pickup": "Changi Airport",
  "dropoff": "Marina Bay Sands",
  "date": "Tomorrow",
  "time": "08:00 PM"
}
```

## Malaysia Malay

Input:
`Saya mahu pergi dari KLIA ke Bukit Bintang esok jam 10 pagi.`

Expected:
```json
{
  "pickup": "Kuala Lumpur International Airport",
  "dropoff": "Bukit Bintang",
  "time": "10:00 AM"
}
```

## UAE Arabic

Input:
`I need a car from Dubai Airport to Burj Khalifa tomorrow 10 morning.`

Expected:
```json
{
  "pickup": "Dubai Airport",
  "dropoff": "Burj Khalifa",
  "time": "10:00 AM"
}
```

## France French

Input:
`Je veux aller de l'aeroport Charles de Gaulle a la Tour Eiffel demain.`

Expected:
```json
{
  "pickup": "Charles de Gaulle Airport",
  "dropoff": "Eiffel Tower",
  "date": "Tomorrow"
}
```

## Japan Japanese

Input:
`Tomorrow 10 AM from Narita Airport to Tokyo Station.`

Expected:
```json
{
  "pickup": "Narita Airport",
  "dropoff": "Tokyo Station",
  "time": "10:00 AM"
}
```

## Dynamic Update

Input:
`Update the dropoff location to Villivakkam.`

Expected:
```json
{
  "dropoff": "Villivakkam"
}
```

Input:
`Change the contact name to Bharathi.`

Expected:
```json
{
  "name": "Bharathi"
}
```

## Phone Validation

Valid India:
`9876543210`

Invalid India:
`1234567890`

Expected invalid reply:
`That mobile number does not look valid for the selected country. Please share it again with country code if needed.`
