import React, { useState, useEffect } from 'react';
import axios from 'axios';
import map from './map.png';
import './App.css';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';


function App() {
  const [coordinates, setCoordinates] = useState({ x: '', y: '' });
  const [selectedItem, setSelectedItem] = useState('');
  const [selectedGridCoordinates, setSelectedGridCoordinates] = useState({ x: null, y: null });
  const [data, setData] = useState();
  const [intervalId, setIntervalId] = useState(null); // Store intervalId in state

  // const data = {"endoscopeShyam": {"x": 1, "y": 4}, "endoscopeJeff": {"x": 5, "y": 2}}
  // const endoscopeJeffX = data.endoscopeJeff.x;
  // console.log(endoscopeJeffX); // prints 5
  

  const handleCoordinateChange = (event, axis) => {
    const newCoordinates = { ...coordinates, [axis]: event.target.value };
    setCoordinates(newCoordinates);
  };

  const id = setInterval(() => {
    axios.get('http://192.168.229.162:8015/data')
      .then(response => {
        setData(response.data)
        setSelectedGridCoordinates({ x: parseInt(response.data.endo_shyam.x), y: parseInt(response.data.endo_shyam.y) });
        setCoordinates({ x: response.data.endo_shyam.x, y: response.data.endo_shyam.y }); // Update X and Y coordinates

        })
      .catch(error => console.log(error));
  }, 5000);


  return (
  <div className="App">
    <div className="App-header">
      <div className="coordinates">
        <label htmlFor="x-coordinate"> X: </label>
        <input id="x-coordinate" type="text" value={coordinates.x} onChange={(e) => handleCoordinateChange(e, 'x')} />
        <label htmlFor="y-coordinate"> Y: </label>
        <input id="y-coordinate" type="text" value={coordinates.y} onChange={(e) => handleCoordinateChange(e, 'y')} />
      </div>
      <div className="container">
        <div className="grid-container">
          <img src={map} alt="Map" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          <div className="grid-overlay">
            {[...Array(10)].map((_, rowIndex) => (
              <div className="grid-row" key={rowIndex}>
                {[...Array(10)].map((_, colIndex) => (
                    <div
                      // className={`grid-cell${
                      //   data.endoscopeShyam.x === colIndex && data.endoscopeShyam.y === rowIndex ? ' selected' : ''                      
                      // }`}
                      className={`grid-cell${
                        data.endo_shyam.x === colIndex && data.endo_shyam.y === rowIndex ? ' selected' : ''
                      }${
                        data.endo_jw.x === colIndex && data.endo_jw.y === rowIndex ? ' selected1' : ''
                      }${
                        data.endo_shyam.x === colIndex && data.endo_shyam.y === rowIndex && data.endo_jw.x === colIndex && data.endo_jw.y === rowIndex ? ' sameSelected' : ''
                      }`}
                      key={`${rowIndex}-${colIndex}`}
                    />
                ))}
              </div>
            ))}
          </div>
        </div>
        <Box>
        Legend:
          <List>
              <ListItem className='text'>
              endoscopeShyam
              </ListItem>
              <ListItem className='text1'>
              endoscopeJeff
              </ListItem>
            </List>
        </Box>

      </div>
    </div>
  </div>
  );
}

export default App;