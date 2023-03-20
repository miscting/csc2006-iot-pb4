import React, { useState, useEffect } from 'react';
import axios from 'axios';
import map from './map.png';
import './App.css';

function App() {
  const [coordinates, setCoordinates] = useState({ x: '', y: '' });
  const [selectedItem, setSelectedItem] = useState('');
  const [selectedGridCoordinates, setSelectedGridCoordinates] = useState({ x: null, y: null });
  const [data, setData] = useState({});
  const [intervalId, setIntervalId] = useState(null); // Store intervalId in state
  let x = 0;
  let y = 0;

  useEffect(() => {
    return () => {
      // Clean up the interval when the component unmounts or the selectedItem changes
      clearInterval(intervalId);
    };
  }, [intervalId, selectedItem]);

  const handleCoordinateChange = (event, axis) => {
    const newCoordinates = { ...coordinates, [axis]: event.target.value };
    setCoordinates(newCoordinates);
  };

  const handleItemSelection = (event) => {
    const selectedItem = event.target.value;
    setSelectedItem(selectedItem);

    clearInterval(intervalId); // Clear the previous interval
    // Set selected grid coordinates based on selected item
    switch (selectedItem) {
      case 'A':
        const id = setInterval(() => {
          // x = x + 1;
          // y = y + 1;
          // setSelectedGridCoordinates({ x: x, y: y });
          // setCoordinates({ x: x, y: y });
          axios.get('http://192.168.229.162:8015/data')
            .then(response => {
                setSelectedGridCoordinates({ x: parseInt(response.data.x), y: parseInt(response.data.y) });
                setCoordinates({ x: response.data.x, y: response.data.y }); // Update X and Y coordinates
              })
            .catch(error => console.log(error));
        }, 5000);
        setIntervalId(id); // Store the new intervalId in state
        break;
      case 'B':
        setSelectedGridCoordinates({ x: 8, y: 2 });
        setCoordinates({ x: '1.3712772', y: '103.8394046' });
        break;
      case 'C':
        setSelectedGridCoordinates({ x: 3, y: 7 });
        setCoordinates({ x: '1.3591946', y: '103.8270986' });
        break;
      default:
        setSelectedGridCoordinates({ x: null, y: null });
    }
  };


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
                    className={`grid-cell${
                      selectedGridCoordinates.x === colIndex && selectedGridCoordinates.y === rowIndex ? ' selected' : ''
                    }`}
                    key={`${rowIndex}-${colIndex}`}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
        <div className="item-list">
          <label>Choose an Endoscope:</label>
          <br />
          <label>
            <input type="radio" name="item" value="A" checked={selectedItem === 'A'} onChange={handleItemSelection} /> Endoscope A
          </label>
          <br />
          <label>
            <input type="radio" name="item" value="B" checked={selectedItem === 'B'} onChange={handleItemSelection} /> Endoscope B
          </label>
          <br />
          <label>
            <input type="radio" name="item" value="C" checked={selectedItem === 'C'} onChange={handleItemSelection} /> Endoscope C
          </label>
          <br />
        </div>
      </div>
    </div>
  </div>
  );
}

export default App;