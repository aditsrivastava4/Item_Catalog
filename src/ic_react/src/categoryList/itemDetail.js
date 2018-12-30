import React, { Component } from 'react';
import Cookies from 'js-cookie';

class ItemDetail extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: false,
            error: null,
            itemData: null
        }
        this.getItemDetail()
    }

    getItemDetail() {
        let url = "/catalog/" + this.props.itemData.book + "/"+ this.props.itemData.itemID
        fetch(url, {
            method: 'POST',
        })
        .then((response) => {
            return response.json()
        })
        .then((result) => {
            this.setState({
                isLoaded: true,
                itemData: result.item
            })
        })
    }

    render() {
        const { loggedIn, isLoaded, error, itemData } = this.state
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                            <h1>Book</h1>
                        </div>
                    </div>
                    <div className="row">
                        <div class="col-sm-2 col-md-2 col-lg-2"></div>
                        <div id="bgColor" className="col-sm-8 col-md-8 col-lg-8">
                            
                            <h2>{ itemData.item }</h2>
                            <h5>Author: { itemData.author }</h5>
                            <h5>Publisher : { itemData.publisher }</h5>
                            <h4>Description</h4>
                            <p>{ itemData.description }</p>
                            { loggedIn ?
                                <p>
                                    <a className="btn btn-default"><span className="glyphicon glyphicon-edit"></span> Edit</a>&nbsp;
                                    <p onClick={ this.props.onDelete } className="btn btn-default">
                                        <span className="glyphicon glyphicon-trash"></span>
                                        Delete
                                    </p>
                                </p> :
                                ""
                            }

                        </div>
                        <div class="col-sm-2 col-md-2 col-lg-2"></div>
                    </div>
                </div>
            )
        }
    }
}

export default ItemDetail;