import axios from "axios";
import PropTypes from "prop-types";
import React from "react";
import { useQuery } from "react-query";

const Clanmate = ({ id }) => {
	const { isLoading, isError, data, error } = useQuery(["chars"], () =>
		axios.get(`http://127.0.0.1:8000/guardians/id/${id}`).then((res) => res.data)
	);


	if (isLoading) return "Loading...";
	if (isError) return `Error: ${error.message}`;

	return (
		<div>
				<div> {data.name} 					
					{/* {data.map((char) => (
						<div key={char.id}>
							{char.name} {char.id}
						</div>
					))} */}
				</div>
		</div>
	);
};

Clanmate.propTypes = {
	id: PropTypes.number.isRequired,
};

export default Clanmate;
