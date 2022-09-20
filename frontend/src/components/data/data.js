import React, {Component} from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CircularProgress from '@mui/material/CircularProgress'

export default class Data extends Component {
    constructor(props){
        super(props);
        this.state = {
            data: [],
            head: []
          }
        // this.renderListItems = this.renderListItems.bind(this)
    }
  componentDidMount() {
    fetch('get_data').then(
        results => results.json()
    ).then(
        data =>
        {
        this.setState({head: Object.keys(data), data: data})
        Object.keys(data).map(item => {
        const div = document.getElementById(item)
        console.log(div, item)
        this.state.data[item].map(i => {
            let text = document.createElement('p');
            text.innerHTML = i
            div.appendChild(text)
  })})})
    // return [
    //   <li key={1}><a href="#">Link1</a></li>,
    //   <li key={2}><a href="#">Link2</a></li>,
    //   <li key={3} className="active">Active item</li>,
    // ]
  }
    render () {  
        return (
      <div>
        {this.state.data ?
        Object.keys(this.state.data).map(item => {
            return(<Accordion>
                <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
                >
                <Typography>{item}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <div id={item}>
                    </div>
                </AccordionDetails>
            </Accordion>) }): <CircularProgress />
        }
      </div>
      );
    }
}