// import React, { useState } from 'react';
// import map from './map.png';
// import './App.css';

// function App() {
//   const [coordinates, setCoordinates] = useState({ x: '', y: '' });
//   const [selectedItem, setSelectedItem] = useState('');
//   const [selectedGridCoordinates, setSelectedGridCoordinates] = useState({ x: null, y: null });

//   const handleCoordinateChange = (event, axis) => {
//     const newCoordinates = { ...coordinates, [axis]: event.target.value };
//     setCoordinates(newCoordinates);
//   };

//   const handleItemSelection = (event) => {
//     const selectedItem = event.target.value;
//     setSelectedItem(selectedItem);

//     // Set selected grid coordinates based on selected item
//     switch (selectedItem) { 
//       // Maybe not coordinates, but display the x, y
//       case 'A':
//         setSelectedGridCoordinates({ x: 4, y: 3 });
//         setCoordinates({ x: '1.3652654', y: '103.8458633' }); // Update X and Y coordinates
//         break;
//       case 'B':
//         setSelectedGridCoordinates({ x: 8, y: 2 });
//         setCoordinates({ x: '1.3712772', y: '103.8394046' }); // Update X and Y coordinates
//         break;
//       case 'C':
//         setSelectedGridCoordinates({ x: 3, y: 7 });
//         setCoordinates({ x: '1.3591946', y: '103.8270986' }); // Update X and Y coordinates
//         break;
//       default:
//         setSelectedGridCoordinates({ x: null, y: null });
//     }
//   };


//   return (
//   <div className="App">
//     <div className="App-header">
//       <div className="coordinates">
//         <label htmlFor="x-coordinate"> X: </label>
//         <input id="x-coordinate" type="text" value={coordinates.x} onChange={(e) => handleCoordinateChange(e, 'x')} />
//         <label htmlFor="y-coordinate"> Y: </label>
//         <input id="y-coordinate" type="text" value={coordinates.y} onChange={(e) => handleCoordinateChange(e, 'y')} />
//       </div>
//       <div className="container">
//         <div className="grid-container">
//           <img src={map} alt="Map" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div className="grid-overlay">
//             {[...Array(10)].map((_, rowIndex) => (
//               <div className="grid-row" key={rowIndex}>
//                 {[...Array(10)].map((_, colIndex) => (
//                   <div
//                     className={`grid-cell${
//                       selectedGridCoordinates.x === colIndex && selectedGridCoordinates.y === rowIndex ? ' selected' : ''
//                     }`}
//                     key={`${rowIndex}-${colIndex}`}
//                   />
//                 ))}
//               </div>
//             ))}
//           </div>
//         </div>
//         <div className="item-list">
//           <label>Choose an Endoscope:</label>
//           <br />
//           <label>
//             <input type="radio" name="item" value="A" checked={selectedItem === 'A'} onChange={handleItemSelection} /> Endoscope A
//           </label>
//           <br />
//           <label>
//             <input type="radio" name="item" value="B" checked={selectedItem === 'B'} onChange={handleItemSelection} /> Endoscope B
//           </label>
//           <br />
//           <label>
//             <input type="radio" name="item" value="C" checked={selectedItem === 'C'} onChange={handleItemSelection} /> Endoscope C
//           </label>
//           <br />
//         </div>
//       </div>
//     </div>
//   </div>
//   );
// }

// export default App;