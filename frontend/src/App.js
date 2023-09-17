import React, {useEffect, useState} from 'react';
import QueryInput from "./QueryInput";
import UserQueryDisplay from './UserQueryDisplay';
import SourceOutputList from "./SourceOutputList";

function App() {

    const [userQuery, setUserQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState({
        query: "",
        result: "",
        sources: [],
        state: ""
    });
    const [isDataReceived, setIsDataReceived] = useState(false);


    useEffect(() => {
        if (!userQuery) return; // Don't open a WebSocket if there's no query

        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onopen = () => {
            console.log('WebSocket is connected.');
            ws.send(JSON.stringify({"query": userQuery}));
            setIsLoading(true);
        };

        ws.onmessage = (event) => {
            console.log(`Server says: ${event.data}`);
            const receivedData = JSON.parse(event.data);
            switch (receivedData.state) {
                case "PROCESSING":
                    setIsLoading(true);
                    break;
                case "SUCCESS":
                    setResponse(receivedData);
                    setIsLoading(false);
                    setIsDataReceived(true);
                    break;
                case "":
                    setIsLoading(true);
                    break;
                default:
                    setIsLoading(false);
                    console.error("Unexpected state received");
            }
        };

        ws.onerror = (error) => {
            console.log(`WebSocket error: ${error}`);
            setIsLoading(false);
        };

        return () => {
            ws.close();
        };
    }, [userQuery]);

    // Output
    return (
        <div className="App py-5">
            <header className="App-header">
                <h1>Ask the Patents Act</h1>
            </header>
            <main>
                <QueryInput setUserQuery={setUserQuery}/>
                <hr/>
                {isLoading ? ( // Conditional rendering based on isLoading state
                    <div>Loading...</div> // Your loading screen here
                ) : isDataReceived ? (
                    <>
                        <UserQueryDisplay titleName="You asked..." output={response.query}/>
                        <hr/>
                        <UserQueryDisplay titleName="The legislation answered..." output={response.result}/>
                        <SourceOutputList sources={response.sources || []}/>
                    </>
                ) : null}
            </main>
        </div>
    );
}

export default App;
