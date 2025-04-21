const functions = require("firebase-functions");
const admin = require("firebase-admin");
const axios = require("axios");


admin.initializeApp({
  databaseURL: "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app",
});

//location from Firebase
async function fetchLocationFromFirebase() {
  try {
    const locationRef = admin.database().ref("location");
    const snapshot = await locationRef.once("value");
    const locationData = snapshot.val();
    console.log("Fetched location data:", locationData);
    if (typeof locationData === "string") {
      return locationData;
    }
    throw new Error("City not found");
  } catch (error) {
    console.error("Error fetching location from Firebase:", error);
    return null;
  }
}

async function fetchWeatherData(city) {
  const apiKey = process.env.OPENWEATHER_API_KEY;
  const url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
  try {
    const response = await axios.get(url);
    const data = response.data;
    const temperature = data.main.temp;
    const timestamp = new Date().toISOString();
    const date = new Date().toLocaleDateString();
    const day = new Date().toLocaleDateString("en-US", { weekday: "long" });
    return {
      temperature,
      timestamp,
      date,
      day,
    };
  } catch (error) {
    console.error("Error fetching weather data:", error);
    return null;
  }
}

//to firebase
async function sendWeatherDataToFirebase(weatherData) {
  try {
    const weatherRef = admin.database().ref("WeatherData1");
    await weatherRef.push(weatherData);
    console.log("Weather data sent to Firebase:", weatherData);
    return true;
  } catch (error) {
    console.error("Error sending weather data to Firebase:", error);
    return false;
  }
}


exports.scheduledWeatherUpdate = functions.pubsub
  .schedule("every 60 minutes")
  .onRun(async (context) => {
    console.log("Scheduled weather update triggered");

    const city = await fetchLocationFromFirebase();
    if (!city) {
      console.log("No location found in Firebase");
      return { success: false, message: "No location found" };
    }

    const weatherData = await fetchWeatherData(city);
    if (!weatherData) {
      console.log(`Failed to fetch weather data for ${city}`);
      return { success: false, message: `Failed to fetch weather data for ${city}` };
    }

    const success = await sendWeatherDataToFirebase(weatherData);
    if (success) {
      console.log(`Successfully updated weather data for ${city}`);
      return { success: true, message: `Weather data for ${city} updated successfully` };
    } else {
      console.log("Failed to save weather data to Firebase");
      return { success: false, message: "Failed to save weather data" };
    }
  });

//manual trigger
exports.updateWeatherManual = functions.https.onRequest(async (req, res) => {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    console.log("Manual weather update triggered");

    const city = await fetchLocationFromFirebase();
    if (!city) {
      return res.status(400).json({ error: "No location found in Firebase" });
    }

    const weatherData = await fetchWeatherData(city);
    if (weatherData) {
      const success = await sendWeatherDataToFirebase(weatherData);
      if (success) {
        return res.status(200).json({ success: true, data: weatherData });
      }
    }

    return res.status(500).json({ error: "Failed to process weather data" });
  } catch (error) {
    console.error("Error in manual weather update:", error);
    return res.status(500).json({ error: error.message });
  }
});