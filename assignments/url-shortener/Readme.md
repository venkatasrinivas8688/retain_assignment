
Note:In this assignment i have used node.js with express and MongoDB Database to develop URL Shorter Service.

->What is a URL Shortening Service?
Ans->A URL shortening service like Bit.ly or TinyURL converts a long, hard-to-share URL into a shorter, more manageable code.
Example:
Original URL:https://www.youtube.com/watch?v=dQw4w9WgXcQ
shortened URL:https://bit.ly/abc123
->When someone visits bit.ly/abc123, they are redirected to the original long URL.

Implementtion:
1)Here first have implemented express server by initialising to port 5000
2)Go to mongoDB Database get the connection url connect the database to express server 
3)Implement schema design 
4)Implemented Routes with appropriate error handling and status codes  

for test cases:
  ->I have taken help from Chat Gpt for this section because of using external libraries like Mocha(test runner),Chai(assertion library), and Chai HTTP(to simulate HTTP request.

const chai = require('chai');
->Imports Chai,the asertion library 

const chaiHttp = require('chai-http');
->Imports the Chai plugin that allows you to make HTTP requests for testing.

const { expect } = chai;
->Extracts the expect assertion style from Chai (e.g., expect(value).to.equal(...)).

chai.use(chaiHttp);
->Tells Chai to use the HTTP request plugin.

describe('URL Shortener API', () => {}
->Defines a test group. All it() test cases below are grouped under this label.

Runs Before All Tests and Connects to the MongoDB test database.
  before(async () => {
    await mongoose.connect(process.env.MONGO_URI);
  });

After All Tests ,Clears the urls collection so tests don’t affect each other and Disconnects MongoDB cleanly.
  after(async () => {
    await Url.deleteMany({});
    await mongoose.disconnect();
  });
