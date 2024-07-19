import './App.css';
import axios from 'axios';
function App() {

  const changeContent=async ()=>{
    let obj = {
      "username": "attendee3",
      "password" : "attendee3"
    }

    
    let result = await axios.post("http://localhost:8000/user" , obj)
    console.log(result)
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={changeContent}>Change the Content</button>
      </header>
    </div>
  );
}

export default App;
