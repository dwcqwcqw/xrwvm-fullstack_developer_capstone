import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  const [purchase, setPurchase] = useState("no");
  const navigate = useNavigate();

  const { id } = useParams();
  const BACKEND_URL = "http://localhost:8000";
  const DATABASE_URL = "http://localhost:3030";
  const dealer_url = `${BACKEND_URL}/djangoapp/dealer/${id}`;
  const review_url = `${DATABASE_URL}/insert_review`;
  const carmodels_url = `${BACKEND_URL}/djangoapp/get_cars`;

  // Check login status
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/djangoapp/current_user`, {
          credentials: 'include'
        });
        const data = await response.json();
        setIsLoggedIn(data.isLoggedIn);
        setUserName(data.username || "");
      } catch (error) {
        console.error("Error checking login status:", error);
        setIsLoggedIn(false);
      }
    };
    checkLoginStatus();
  }, []);

  const postreview = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (!isLoggedIn) {
      setError("Please login to submit a review");
      setLoading(false);
      return;
    }

    try {
      const reviewData = {
        name: userName,
        dealership: id,
        review: review,
        purchase: purchase === "yes",
        purchase_date: date,
        car_make: model.split(' ')[0],
        car_model: model.split(' ').slice(1).join(' '),
        car_year: year
      };

      console.log("Submitting review:", reviewData);

      const response = await fetch(`${DATABASE_URL}/insert_review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reviewData)
      });

      const data = await response.json();
      console.log("Response:", data);

      if (response.ok) {
        alert("Review submitted successfully!");
        // Redirect to dealer page
        navigate(`/dealer/${id}`);
        window.location.reload(); // Refresh to show new review
      } else {
        throw new Error(data.message || "Failed to submit review");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      setError(`Failed to submit review: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const data = await res.json();
      if (data.status === 200 && data.dealer) {
        setDealer(data.dealer[0]);
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
      setError("Failed to load dealer information");
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url);
      const data = await res.json();
      setCarmodels(data.CarModels || []);
    } catch (error) {
      console.error("Error fetching car models:", error);
      setError("Failed to load car models");
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from(
    { length: currentYear - 2014 },
    (_, i) => currentYear - i
  );

  return (
    <div className="post-review-container">
      <div className="review-header">
        <h1>{dealer.full_name}</h1>
        <p className="dealer-location">
          {dealer.city}, {dealer.address} - {dealer.zip}, {dealer.state}
        </p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="review-form">
        {!isLoggedIn && (
          <div className="login-warning">
            Please <a href="/login">login</a> to submit a review
          </div>
        )}
        
        <div className="form-group">
          <label>Did you purchase a vehicle?</label>
          <select
            value={purchase}
            onChange={(e) => setPurchase(e.target.value)}
          >
            <option value="no">No</option>
            <option value="yes">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Review Content</label>
          <textarea
            placeholder="Share your experience with this dealership..."
            rows="5"
            value={review}
            onChange={(e) => setReview(e.target.value)}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Purchase Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              max={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="form-group">
            <label>Car Model</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
            >
              <option value="">Select Car Make and Model</option>
              {carmodels.map((carmodel, index) => (
                <option key={index} value={`${carmodel.CarMake} ${carmodel.CarModel}`}>
                  {carmodel.CarMake} {carmodel.CarModel}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Car Year</label>
            <select
              value={year}
              onChange={(e) => setYear(e.target.value)}
            >
              <option value="">Select Year</option>
              {yearOptions.map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>
        </div>

        <button 
          className="submit-review" 
          onClick={postreview}
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit Review"}
        </button>
      </div>
    </div>
  );
};

export default PostReview;
