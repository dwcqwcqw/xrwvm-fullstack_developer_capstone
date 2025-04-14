import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png"
import neutral_icon from "../assets/neutral.png"
import negative_icon from "../assets/negative.png"
import review_icon from "../assets/reviewbutton.png"

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  const { id } = useParams();
  const BACKEND_URL = "http://localhost:8000";
  const DATABASE_URL = "http://localhost:3030";
  const dealer_url = `${BACKEND_URL}/djangoapp/dealer/${id}`;
  const reviews_url = `${DATABASE_URL}/fetchReviews/dealer/${id}`;
  const post_review = `/postreview/${id}`;
  
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();
      
      if (retobj.status === 200 && retobj.dealer) {
        setDealer(retobj.dealer[0]);
      } else {
        console.error('Error fetching dealer:', retobj);
      }
    } catch (error) {
      console.error('Error fetching dealer:', error);
    }
  }

  const get_reviews = async () => {
    try {
      console.log('Fetching reviews from:', reviews_url);
      const res = await fetch(reviews_url);
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const reviews = await res.json();
      console.log('Received reviews:', reviews);
      
      if (Array.isArray(reviews) && reviews.length > 0) {
        setReviews(reviews);
        setUnreviewed(false);
      } else {
        console.log('No reviews found');
        setUnreviewed(true);
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setUnreviewed(true);
    }
  }

  const senti_icon = (sentiment) => {
    return sentiment === "positive" ? positive_icon : 
           sentiment === "negative" ? negative_icon : 
           neutral_icon;
  }

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review} className="write-review-button">
          <img src={review_icon} alt='Write a review'/>
          Write a review
        </a>
      );
    }
  }, []);

  return (
    <div className="dealer-container">
      <div className="dealer-header">
        <h1 className="dealer-title">
          {dealer.full_name}
          {postReview}
        </h1>
        <h3 className="dealer-address">
          {dealer.city}, {dealer.address} - {dealer.zip}, {dealer.state}
        </h3>
      </div>

      <div className="reviews-container">
        {reviews.length === 0 && !unreviewed ? (
          <div className="loading-reviews">Loading Reviews....</div>
        ) : unreviewed ? (
          <div className="no-reviews">No reviews yet!</div>
        ) : (
          reviews.map((review, index) => (
            <div key={index} className='review-card'>
              <div className="review-header">
                <img 
                  src={senti_icon(review.sentiment)} 
                  className="sentiment-icon" 
                  alt={review.sentiment}
                />
                <span className="review-car-info">
                  {review.car_make} {review.car_model} {review.car_year}
                </span>
              </div>
              <div className='review-content'>{review.review}</div>
              <div className="review-footer">
                <span className="reviewer-name">{review.name}</span>
              </div>
            </div>
          ))
        )}
      </div>  
    </div>
  );
}

export default Dealer;
