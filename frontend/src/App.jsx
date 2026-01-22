function App() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login/google-oauth2/";
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>OAuth Test</h1>
      <button onClick={handleLogin}>
        Login with Google
      </button>
    </div>
  );
}

export default App;