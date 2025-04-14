const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const fs = require('fs');
const Review = require('./review');
const Dealership = require('./dealership');

// Enable CORS for all routes
const corsOptions = {
    origin: 'http://localhost:3000',
    credentials: true,
    optionsSuccessStatus: 200
};

// Create Express app
const app = express();
app.use(cors(corsOptions));
app.use(express.json());

// Connect to MongoDB
const mongoHost = process.env.MONGO_HOST || 'mongo_db';
const mongoPort = process.env.MONGO_PORT || '27017';
const dbName = 'dealershipsDB';

mongoose.connect(`mongodb://${mongoHost}:${mongoPort}/`, {
    dbName: dbName,
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
    initializeData();
});

// Initialize data from JSON files
async function initializeData() {
    try {
        // Load and insert reviews
        const reviewsData = JSON.parse(fs.readFileSync('./data/reviews.json', 'utf8'));
        await Review.deleteMany({});
        await Review.insertMany(reviewsData.reviews);
        console.log('Reviews data initialized');

        // Load and insert dealerships
        const dealershipsData = JSON.parse(fs.readFileSync('./data/dealerships.json', 'utf8'));
        await Dealership.deleteMany({});
        await Dealership.insertMany(dealershipsData.dealerships);
        console.log('Dealerships data initialized');
    } catch (error) {
        console.error('Error initializing data:', error);
    }
}

// API Routes
app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the Mongoose API' });
});

// Get all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const reviews = await Review.find({});
        res.json(reviews);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching reviews' });
    }
});

// Get reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const reviews = await Review.find({ dealership: req.params.id });
        res.json(reviews);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealer reviews' });
    }
});

// Get all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const dealerships = await Dealership.find({});
        res.json(dealerships);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealerships' });
    }
});

// Get dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const dealerships = await Dealership.find({ state: req.params.state });
        res.json(dealerships);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealerships by state' });
    }
});

// Get dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const dealership = await Dealership.findOne({ id: req.params.id });
        res.json(dealership);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealer' });
    }
});

// Insert a new review
app.post('/insert_review', async (req, res) => {
    try {
        const reviewData = req.body;
        const maxIdReview = await Review.findOne().sort('-id');
        let nextId = 1;

        if (maxIdReview) {
            nextId = maxIdReview.id + 1;
        }

        const newReview = new Review({
            id: nextId,
            name: reviewData.name,
            dealership: reviewData.dealership,
            review: reviewData.review,
            purchase: reviewData.purchase,
            purchase_date: reviewData.purchase_date,
            car_make: reviewData.car_make,
            car_model: reviewData.car_model,
            car_year: reviewData.car_year
        });

        await newReview.save();
        res.status(201).json({
            message: 'Review inserted successfully',
            review: newReview
        });
    } catch (error) {
        console.error('Error inserting review:', error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Start server
const port = process.env.PORT || 3030;
app.listen(port, () => console.log(`Server running on port ${port}`));
