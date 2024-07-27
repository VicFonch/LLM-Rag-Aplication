import "./styles/Sidebar.css";
import { assets } from "../assets/assets";
import { useState } from "react";

export const Sidebar = () => {
  const [extended, setExtended] = useState(true);

  return (
    <div className="sidebar">
      <div className="top">
        <img
          onClick={() => setExtended((prev) => !prev)}
          className="menu"
          src={assets.menu_icon}
          alt=""
        />
        <div className="new-chat">
          <img className="add-icon" src={assets.add_icon} alt="" />
          {extended ? <p>New Chat</p> : null}
        </div>
        {extended ? (
          <div className="recent">
            <p className="recent-title">Recent</p>
            <div className="recent-entry">
              <img src={assets.message_icon} alt="" />
              <p>What's new ...</p>
            </div>
          </div>
        ) : null}
      </div>
      <div className="bottom">
        <div className="botton-item recent-entry">
          <img src={assets.help_icon} alt="" />
          {extended ? <p>Help</p> : null}
        </div>
        <div className="botton-item recent-entry">
          <img src={assets.history_icon} alt="" />
          {extended ? <p>Help</p> : null}
        </div>
      </div>
    </div>
  );
};
