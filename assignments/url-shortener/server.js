require("dotenv").config();
console.log(process.env.PORT);
console.log(process.env.MONGO_URI);

console.log(process.env.BASE_URL);

const express = require("express");
const mongoose = require("mongoose");
const urlRoutes = require("./routes/urlRoutes");

const app = express();
app.use(express.json());
app.use("/api", urlRoutes);

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    app.listen(process.env.PORT, () => {
      console.log(`Server running on http://localhost:${process.env.PORT}`);
    });
  })
  .catch((err) => console.error("MongoDB connection failed:", err));
