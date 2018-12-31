import React, { Component } from 'react';
import Category from './category';
import ItemDetail from './itemDetail';
import Cookies from 'js-cookie';

class CategoryIndex extends Component {
    constructor(props) {
        super(props);
        this.state = {
            onChange: false,
            itemData: null
        }
        this.itemDetail = this.itemDetail.bind(this)
        this.deleteOnClick = this.deleteOnClick.bind(this)
    }
    
    itemDetail(event) {
        this.setState({
            onChange: true,
            itemData: {
                book: event.currentTarget.innerText.split('\n')[0],
                itemID: event.currentTarget.firstElementChild.innerText
            }
        })
        event.preventDefault()
    }

    // Delete an Item
    deleteOnClick(event) {
        let url = "/catalog/"+ this.state.itemData.itemID +"/delete"
        fetch(url, {
            method: 'POST',
            body: Cookies.get("uid")
        })
        .then((response) => {
            return response.json()
        })
        .then((result) => {
            if(result.code == 200) {
                this.setState({
                    onChange: false,
                    itemData: null
                })
            } else if(result.code == 404) {
                window.location.href = '/login'
            } else if(result.code == 400) {
                alert('Bad Request')
                window.location.href = '/'
            }
        })
        event.preventDefault()
    }

    render() {
        return (
            <div>
                { this.state.onChange ?
                    <ItemDetail
                        itemData = { this.state.itemData }
                        onDelete = { this.deleteOnClick }
                        CategoryName={ this.props.CategoryName } /> :
                    <Category itemClick={ this.itemDetail } CategoryName={ this.props.CategoryName }/>
                }
            </div>
        );
    }
}

export default CategoryIndex;