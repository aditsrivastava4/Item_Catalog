import React, { Component } from 'react';
import Catalog from './getdata/catalog'
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Catalog />
      </div>
    );
  }
}

export default App;
