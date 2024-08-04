import "./styles/Main.css";
import { Chat } from "../components/Chat";
import { Sidebar } from "../components/Sidebar";

export const Main = () => {
  return (
    <div className="page__main-container">
      <Sidebar />
      <Chat />
    </div>
  );
};
