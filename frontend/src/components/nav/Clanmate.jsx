import PropTypes from "prop-types";
import React from "react";

const Clanmate = ({ id }) => {
    const { isLoading, isError, data, error, refetch } = useQuery(["chars"], () =>
			axios.get("localhost").then((res) => res.data)
		);


	return <div>Clanmate {id} </div>;
};

Clanmate.propTypes = {
	id: PropTypes.number.isRequired,
};

export default Clanmate;
