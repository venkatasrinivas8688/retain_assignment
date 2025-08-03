const chai = require("chai");
const chaiHttp = require("chai-http");
const app = require("../server"); // Make sure to export app in server.js if needed
const Url = require("../models/Url");
const mongoose = require("mongoose");
const { expect } = chai;
chai.use(chaiHttp);

describe("URL Shortener API", () => {
  before(async () => {
    await mongoose.connect(process.env.MONGO_URI);
  });

  after(async () => {
    await Url.deleteMany({});
    await mongoose.disconnect();
  });

  let shortCode;

  it("should shorten a valid URL", async () => {
    const res = await chai
      .request("http://localhost:5000")
      .post("/shorten")
      .send({ originalUrl: "https://www.google.com" });

    expect(res.status).to.equal(201);
    expect(res.body.shortCode).to.have.length(6);
    shortCode = res.body.shortCode;
  });

  it("should not shorten an invalid URL", async () => {
    const res = await chai
      .request("http://localhost:5000")
      .post("/shorten")
      .send({ originalUrl: "invalid-url" });

    expect(res.status).to.equal(400);
  });

  it("should redirect to original URL", async () => {
    const res = await chai
      .request("http://localhost:5000")
      .get(`/${shortCode}`);

    expect(res).to.redirect;
  });

  it("should return 404 for unknown short code", async () => {
    const res = await chai.request("http://localhost:5000").get("/xyz999");

    expect(res.status).to.equal(404);
  });

  it("should return analytics for short code", async () => {
    const res = await chai
      .request("http://localhost:5000")
      .get(`/stats/${shortCode}`);

    expect(res.status).to.equal(200);
    expect(res.body.clickCount).to.be.a("number");
    expect(res.body.originalUrl).to.include("https");
  });
});
