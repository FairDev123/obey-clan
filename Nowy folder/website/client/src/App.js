import './App.css';
import { useState } from 'react';
import Axios from 'axios'

function App() {

  const [discordName, setDiscordName] = useState('');
  const [PixelGunID, setPixelGunID] = useState(0);
  const [PixelGunName, setPixelGunName] = useState('');
  const [ClanRank, setClanRank] = useState('');
  const [Valor, setValor] = useState(0);
  const [ID, setID] = useState(0);

  const [membersList, setMembersList] = useState([])

  const addMember = () => {
    Axios.post('http://localhost:3001/create', {
      id: null,
      discordid: ID,
      discordname: discordName,
      pgid: PixelGunID,
      pgname: PixelGunName,
      rank: ClanRank,
      valors: Valor
    }).then(() => {
      console.log("success")
    })
  }
  const getMembers = () => {
    Axios.get('http://localhost:3001/get').then((response) => {
      console.log(response)
    })
  }


  return (
    <div className="App">
      <div className="information">
        <label><b>Discord ID</b></label>
        <input type="number" onChange={(event) => {
          setID(event.target.value);
        }}
          />
        <label><b>Discord Name</b></label>
        <input type="text" onChange={(event) => {
          setDiscordName(event.target.value);
        }}
          />
        <label><b>Pixel Gun ID</b></label>
        <input type="number" onChange={(event) => {
          setPixelGunID(event.target.value);
        }}
          />
        <label><b>Pixel Gun Name</b></label>
        <input type="text" onChange={(event) => {
          setPixelGunName(event.target.value);
        }}
          />
        <label><b>Clan Rank</b></label>
        <input type="text" onChange={(event) => {
          setClanRank(event.target.value);
        }}
          />
        <label><b>Valor Points</b></label>
        <input type="number" onChange={(event) => {
          setValor(event.target.value);
        }}
          />
        <button onClick={addMember}>Add member</button>
        <div className='showMembers'>
          <button onClick={getMembers}>Show members</button>
        </div>
      </div>
    </div>
  );
}

export default App;
