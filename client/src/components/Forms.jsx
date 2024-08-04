import "./styles/Forms.css";
import axios from "axios";

export const FormLogin = () => {
  const api_url = import.meta.env.APP_API_BASE_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const username = e.target[0].value;
    const password = e.target[1].value;
    const userData = new URLSearchParams();
    userData.append("username", username);
    userData.append("password", password);
    try {
      const response = await axios.get(`${api_url}/api/login/`, userData);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export const FormSignup = () => {
  return (
    <div className="form-container">
      <h2>Signup</h2>
      <form>
        <input type="text" placeholder="Username" />
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button type="submit">Signup</button>
      </form>
    </div>
  );
};
