import React, { Component } from 'react';
import Cookies from 'js-cookie';
import EditNewForm from './edit_new/EditNewForm';

class Category extends Component {
    constructor(props) {
        super(props)
        this.state = {
            itemsList: null,
            category: props.CategoryName,
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: false,
            error: null,
            addItem: false
        }
        this.getItems()
        this.addNewItem = this.addNewItem.bind(this)
    }
    
    getItems() {
        let data = [];
        let url = "/API/"+ this.state.category +"/items.json"
        fetch(url, {
            method: 'POST'
        })
            .then(items => items.json())
            .then((result) => {
                result.items.forEach(item => {
                    data.push({
                        Book: item[0],
                        Author: item[1],
                        itemId: item[2]
                    })
                });
                this.setState({
                    isLoaded: true,
                    itemsList: data
                })
            })
    }

    addNewItem() {
        this.setState({
            addItem: !this.state.addItem
        })
        if(!this.state.addItem) {
            this.getItems()
        }
    }

    render() {
        const { itemsList, category, loggedIn, error, isLoaded, addItem } = this.state
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    {!addItem ?
                        <div className="container">
                            <div className="row">
                                <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                                    <h1>Category: { category }</h1>
                                    { loggedIn ? 
                                        <p>
                                            <a onClick={ this.addNewItem } className="btn btn-primary"><span className="glyphicon glyphicon-plus"></span> Add Book</a>
                                        </p> :
                                        ""
                                    }
                                </div>
                            </div>
                            {   
                                itemsList.map((item) => {
                                    return (
                                        <div className="row">
                                            <div className="col-sm-2 col-md-2 col-lg-2"></div>
                                            <div onClick={ this.props.itemClick } id="bgColor" className="col-sm-8 col-md-8 col-lg-8 pointer text-center category">
                                                <p className="hidden">{ item.itemId }</p>
                                                <h2>{ item.Book }</h2>
                                                <h5><strong>Author:</strong> { item.Author }</h5>
                                            </div>
                                            <div className="col-sm-2 col-md-2 col-lg-2"></div>
                                        </div>
                                    )
                                })
                            }
                        </div> :
                        <EditNewForm
                            afterUpdate = { this.addNewItem }
                            option = { "New" }
                            itemData = {{
                                item: "Book's Name",
                                author: "Author's Name",
                                description: "Book's Description",
                                publisher: "Publisher's Name"
                            }}
                            CategoryName={ category } />
                    }
                </div>
            )
        }
    }
}

export default Category;