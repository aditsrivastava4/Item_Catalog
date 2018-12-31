import React, { Component } from 'react';
import Cookies from 'js-cookie';
import EditNewForm from './edit_new/EditNewForm';

class ItemDetail extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: false,
            error: null,
            itemData: null,
            toEdit: false
        }
        this.getItemDetail()
        this.editItem = this.editItem.bind(this)
        this.changeEditState = this.changeEditState.bind(this)
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

    changeEditState() {
        console.log(this.state)
        this.setState({
            toEdit: !this.state.toEdit
        })
        console.log(this.state)
    }

    editItem(event) {
        this.changeEditState()
        event.preventDefault()
    }

    render() {
        const { loggedIn, isLoaded, error, itemData, toEdit } = this.state
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    { !toEdit ?
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
                                            <p onClick={ this.editItem } className="btn btn-default">
                                                <span className="glyphicon glyphicon-edit"></span>
                                                Edit
                                            </p>&nbsp;
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
                        </div> :
                        <EditNewForm afterUpdate = { this.changeEditState } option = { "Edit" } itemData = { itemData } CategoryName={ this.props.CategoryName } />
                    }
                </div>
            )
        }
    }
}

export default ItemDetail;