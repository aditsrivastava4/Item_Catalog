import React, { Component } from 'react';
import Cookies from 'js-cookie';

class Category extends Component {
    constructor(props) {
        super(props)
        this.state = {
            itemsList: null,
            category: props.CategoryName,
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: false,
            error: null
        }
        this.getItems()
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
                        Author: item[1]
                    })
                });
                this.setState({
                    isLoaded: true,
                    itemsList: data
                })
            })
    }
    render() {
        const { itemsList, category, loggedIn, error, isLoaded } = this.state
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                            <h1>Category: { category }</h1>
                            { loggedIn ? 
                                <p>
                                    <a href="new">Add Book</a>
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
                                    <div id="bgColor" className="col-sm-8 col-md-8 col-lg-8 text-center category">
                                        <h2>{ item.Book }</h2>
                                        <h5>Author: { item.Author }</h5>
                                    </div>
                                    <div className="col-sm-2 col-md-2 col-lg-2"></div>
                                </div>
                            )
                        })
                    }
                </div>
            )
        }
    }
}

export default Category;