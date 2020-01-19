import React from 'react';
import logo from './logo.svg';
import './App.css';

import LoopBoard from './LoopBoard'


function App() {

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          TinyLoops
        </h1>
        {/* <Loop radius="50" stroke="6" progress="75"></Loop> */}
        <LoopBoard loops={[]}></LoopBoard>

      </header>
    </div>
  );
}


export default App;
