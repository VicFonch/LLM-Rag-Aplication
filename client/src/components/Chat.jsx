import "./styles/Chat.css";
import { useState } from "react";
import { assets } from "../assets/assets";
import { Link } from "react-router-dom";

const cardsData = [
  { id: 1, title: "Card 1", description: "Description for Card 1" },
  { id: 2, title: "Card 2", description: "Description for Card 2" },
  { id: 3, title: "Card 3", description: "Description for Card 3" },
  { id: 4, title: "Card 4", description: "Description for Card 4" },
];

export const Chat = () => {
  const [isLogedIn, setIsLogedIn] = useState(false);

  return (
    <div className="main">
      <div className="nav">
        <p>The Resistance Archive</p>
        {isLogedIn ? (
          <img src={assets.user_icon} alt="" />
        ) : (
          <div className="nav-links">
            <Link to={"/login"}>
              <button className="login">Login</button>
            </Link>
            <Link to={"/signup"}>
              <button className="signup">Sign Up</button>
            </Link>
          </div>
        )}
      </div>
      <div className="main-container">
        <div className="greet">
          <p>
            <span>Solder, Atten-hut!</span>
          </p>
          <p>
            What do you want to know of <span>WW II</span>
          </p>
        </div>
        <div className="cards">
          {cardsData.map((card) => (
            <div key={card.id} className="card">
              <h3>{card.title}</h3>
              <p>{card.description}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="main-botton">
        <div className="search-box">
          <input type="text" placeholder="Enter the prompt here" />
          <img src={assets.send_icon} alt="" />
        </div>
      </div>
    </div>
  );
};
