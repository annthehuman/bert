import React, {Component} from 'react';
import { BrowserRouter as Routes, Route } from "react-router-dom";
import Home from '../home';

export default class App extends Component {
    constructor(props){
        super(props);
        this.state ={
            experimentLinks: ['1']
        }
    }
    componentDidMount(){
        // console.log('experimentLinks',this.state.experimentLinks)
    }
    render () {return(
        <>
        <Home/>
        </>
    )
    }
}