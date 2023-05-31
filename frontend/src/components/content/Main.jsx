import axios from "axios";
import PropTypes from "prop-types";
import React from "react";
import { useQuery } from "react-query";
import zen from "../../assets/zen.gif";
import Clanmate from "./Clanmate";

const Main = ({ displayedClanmateId }) => {
	const { isLoading, isError, data, error } = useQuery(["chars", displayedClanmateId], () =>
		axios
			.get(`http://127.0.0.1:8000/api/v1/guardians/${displayedClanmateId}`)
			.then((res) => res.data)
	);
	if (isLoading)
		return (
			<div className='flex flex-col w-full lg:overflow-y-auto'>
				<img
					src={zen}
					alt='Loading...'
					className='mx-auto my-auto animate-pulse'></img>
			</div>
		);
	if (isError) return console.log(error);

	return (
		<div className='flex flex-row w-full lg:overflow-y-auto'>
			<Clanmate clanmate={data} />
		</div>
	);
};

Main.propTypes = {
	displayedClanmateId: PropTypes.number.isRequired,
};

export default Main;
