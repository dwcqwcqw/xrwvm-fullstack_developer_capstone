import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const dealer_url = "/djangoapp/get_dealers/";
  
  const filterDealers = async (state) => {
    setLoading(true);
    try {
      let url = dealer_url;
      if (state && state !== "All") {
        url = `/djangoapp/get_dealers/${state}/`;
      }
      console.log('Fetching from URL:', url);
      const res = await fetch(url);
      console.log('Response status:', res.status);
      console.log('Response headers:', res.headers);
      
      // 如果响应不是 JSON，打印原始文本
      const contentType = res.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await res.text();
        console.error('Non-JSON response:', text);
        throw new Error('Server did not return JSON');
      }

      const retobj = await res.json();
      console.log('Response data:', retobj);
      
      if (retobj.status === 200) {
        setDealersList(retobj.dealers || []);
      } else {
        setError(retobj.message || "Failed to fetch dealers");
      }
    } catch (err) {
      console.error('Error details:', err);
      setError(`Error loading dealers: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  const get_dealers = async () => {
    setLoading(true);
    try {
      console.log('Fetching all dealers from:', dealer_url);
      const res = await fetch(dealer_url);
      console.log('Response status:', res.status);
      console.log('Response headers:', res.headers);
      
      // 如果响应不是 JSON，打印原始文本
      const contentType = res.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await res.text();
        console.error('Non-JSON response:', text);
        throw new Error('Server did not return JSON');
      }

      const retobj = await res.json();
      console.log('Response data:', retobj);
      
      if (retobj.status === 200) {
        const all_dealers = retobj.dealers || [];
        const uniqueStates = [...new Set(all_dealers.map(dealer => dealer.state))];
        setStates(uniqueStates);
        setDealersList(all_dealers);
      } else {
        setError(retobj.message || "Failed to fetch dealers");
      }
    } catch (err) {
      console.error('Error details:', err);
      setError(`Error loading dealers: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }
  
  useEffect(() => {
    get_dealers();
  }, []); 

  const isLoggedIn = sessionStorage.getItem("username") != null;
  
  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error</h4>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            <button 
              className="btn btn-outline-danger" 
              onClick={() => get_dealers()}
            >
              Retry
            </button>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <table className='table table-striped'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select 
                name="state" 
                id="state" 
                className="form-select"
                onChange={(e) => filterDealers(e.target.value)}
              >
                <option value="All">All States</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.length > 0 ? (
            dealersList.map(dealer => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td><a href={'/dealer/'+dealer.id}>{dealer.full_name}</a></td>
                <td>{dealer.city}</td>
                <td>{dealer.address}</td>
                <td>{dealer.zip}</td>
                <td>{dealer.state}</td>
                {isLoggedIn && (
                  <td>
                    <a href={`/postreview/${dealer.id}`}>
                      <img src={review_icon} className="review_icon" alt="Post Review"/>
                    </a>
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={isLoggedIn ? 7 : 6} className="text-center">
                No dealers found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers
