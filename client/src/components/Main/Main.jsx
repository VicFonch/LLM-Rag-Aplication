import "./Main.css";
import { assets } from "../../assets/assets";

const cardsData = [
  { id: 1, title: "Card 1", description: "Description for Card 1" },
  { id: 2, title: "Card 2", description: "Description for Card 2" },
  { id: 3, title: "Card 3", description: "Description for Card 3" },
  { id: 4, title: "Card 4", description: "Description for Card 4" },
];

export const Main = () => {
  return (
    <div className="main">
      <div className="nav">
        <p>World War II Assistent</p>
        <img src={assets.user_icon} alt="" />
      </div>
      <div className="main-container">
        <div className="greet">
          <p>
            <span>Hello, Historian</span>
          </p>
          <p>What date do you want to search</p>
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
