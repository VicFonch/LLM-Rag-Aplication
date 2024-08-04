import "./styles/Sidebar.css";
import { assets } from "../assets/assets";
import { useState, useEffect, useRef } from "react";

export const Sidebar = () => {
  const [extended, setExtended] = useState(true);
  const [showHelpBox, setShowHelpBox] = useState(false);
  const helpBoxRef = useRef(null);

  const handleClickOutside = (event) => {
    if (helpBoxRef.current && !helpBoxRef.current.contains(event.target)) {
      setShowHelpBox(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

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
        <div
          className="botton-item recent-entry"
          onClick={() => setShowHelpBox((prev) => !prev)}
        >
          <img src={assets.help_icon} alt="" />
          {extended ? <p>Help</p> : null}
        </div>
        {showHelpBox && (
          <div
            className="help-box"
            ref={helpBoxRef}
          >
            "The Resistance Archive" is an interactive reference system designed
            to explore in depth and detail the events, characters, and key
            moments of World War II. You will speak with General Ollama
            Montgomerry, a war veteran who will guide you through history. Write
            your question and start exploring!
          </div>
        )}
      </div>
    </div>
  );
};
