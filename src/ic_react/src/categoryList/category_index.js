import React, { Component } from 'react';
import Category from './category';
import ItemDetail from './itemDetail';

class CategoryIndex extends Component {
    constructor(props) {
        super(props);
        this.state = {
            onChange: false,
            itemData: null
        }
        this.itemDetail = this.itemDetail.bind(this)
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

    render() {
        return (
            <div>
                { this.state.onChange ?
                    <ItemDetail itemData = { this.state.itemData }/> :
                    <Category itemClick={ this.itemDetail } CategoryName={ this.props.CategoryName }/>
                }
            </div>
        );
    }
}

export default CategoryIndex;