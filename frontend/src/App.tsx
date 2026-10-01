import { useEffect,useState } from "react";

function App() {

  const [backendStatus,setBackendStatus]=useState("Checking...");

  useEffect(()=>{
    fetch("http://127.0.0.1:8000/health")
    .then((response)=>{
      if(!response.ok){
        throw new Error("Backend request failed");
      }
      return response.json(); 
    })
    .then((data)=>{
      setBackendStatus(data.status);
    })
    .catch((error)=>{
      console.error("Backend connection error:",error);
      setBackendStatus("Backend unavailable");
    });
  },[]);

  return (
    <div>
      <h1>AI Productivity Assistant</h1>
      <p>Frontend: Working.</p>
      <p>Backend: {backendStatus}</p>
    </div>
  );
}

export default App;
