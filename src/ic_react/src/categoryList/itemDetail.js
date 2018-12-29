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
            method: 'POST'
        })
        .then((response) => {
            return response.json()
        })
        .then((result) => {
            // console.log(result)
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
                            {/* <div className="row"> */}
                                {/* <div className="col-sm-4 col-md-4 col-lg-4">
                                    <img
                                        src={ itemData.imageURL }
                                        height="300px"
                                        width="250px"
                                        alt={ itemData.item }>
                                    </img>
                                </div> */}
                                {/* <div className="col-sm-8 col-md-8 col-lg-8"> */}
                                    <h2>{ itemData.item }</h2>
                                    <h5>Author: { itemData.author }</h5>
                                    <h5>Publisher : { itemData.publisher }</h5>
                                    <h4>Description</h4>
                                    <p>{ itemData.description }</p>
                                    { loggedIn ?
                                        <p>
                                            <a><span className="glyphicon glyphicon-edit"></span> Edit</a> | 
                                            <a><span className="glyphicon glyphicon-trash"></span> Delete</a>
                                        </p> :
                                        ""
                                    }
                                {/* </div> */}
                            {/* </div> */}
                        </div>
                        <div class="col-sm-2 col-md-2 col-lg-2"></div>
                    </div>
                </div>
            )
        }
    }
}

export default ItemDetail;