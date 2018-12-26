import React, { Component } from 'react';
import Catalog from './getdata/catalog'
import Navbar from './navbar/navbar'
// import logo from './logo.svg';
import './App.css';
import Category from './categoryList/category';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            item: null
        }
        this.itemEvent = this.itemEvent.bind(this)
    }
    itemEvent(event) {
        alert(event.currentTarget.innerText)
        this.setState({
            item:event.currentTarget.innerText
        })
        event.preventDefault()
    }

    render() {
        return (
            <div className="App">
                <Navbar />
                { this.state.item == null?
                    <Catalog ItemClick={ this.itemEvent }/> :
                    <Category CategoryName={ this.state.item }/>
                }
            </div>
        );
    }
}

export default App;
