const express = require("express");
const router = express.Router();
const Url = require("../models/Url");
const validUrl = require("valid-url");
const shortid = require("shortid");
const { BASE_URL } = process.env;

// POST /api/shorten
router.post("/shorten", async (req, res) => {
  const { originalUrl } = req.body;

  if (!validUrl.isWebUri(originalUrl)) {
    return res.status(400).json({ error: "Invalid URL" });
  }

  const shortCode = shortid.generate().slice(0, 6);
  const newUrl = new Url({ originalUrl, shortCode });
  await newUrl.save();

  res.status(201).json({ shortCode, shortUrl: `${BASE_URL}/${shortCode}` });
});

// GET /:shortCode
router.get("/:shortCode", async (req, res) => {
  const { shortCode } = req.params;
  const url = await Url.findOne({ shortCode });

  if (!url) {
    return res.status(404).json({ error: "Short URL not found" });
  }

  url.clickCount++;
  await url.save();

  res.redirect(url.originalUrl);
});

// GET /api/stats/:shortCode
router.get("/stats/:shortCode", async (req, res) => {
  const { shortCode } = req.params;
  const url = await Url.findOne({ shortCode });

  if (!url) {
    return res.status(404).json({ error: "Short URL not found" });
  }

  res.json({
    originalUrl: url.originalUrl,
    shortCode: url.shortCode,
    createdAt: url.createdAt,
    clickCount: url.clickCount,
  });
});

module.exports = router;
