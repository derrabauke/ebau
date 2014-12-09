SELECT  DISTINCT
	"INSTANCE"."INSTANCE_ID",
	"DOSSIERNR"."ANSWER" as "DOSSIER_NR",
	"FORM"."NAME"        as "FORM",
	"LOCATION"."NAME"    as "COMMUNITY",
	"USER"."USERNAME"        AS "USER",
	"ANSWER_PETITION"."ANSWER" AS "PETITION",
	(
		SELECT
			LISTAGG("ANSWER_LIST"."NAME", ', ') WITHIN GROUP (ORDER BY "ANSWER_LIST"."NAME")
		FROM
			table(json_unserialize((
					SELECT
						"ANSWER" as "ANSW"
					FROM
						"ANSWER"
					WHERE
						"ANSWER"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
						AND
						"QUESTION_ID" = 97
						AND
						"CHAPTER_ID" = 21
						AND
						"ITEM" = 1
					))
				)
		JOIN "ANSWER_LIST" ON (
			"VAL" = "ANSWER_LIST_ID"
		)
	) AS "INTENT",
	CASE
		WHEN "ANSWER_STREET_BG"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_BG"."ANSWER"
		WHEN "ANSWER_STREET_NP"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_NP"."ANSWER"
	END AS "STREET",
	GET_STATE_NAME_BY_ID("INSTANCE"."INSTANCE_STATE_ID") AS "STATE",
	"INSTANCE_STATE_DESCRIPTION"."DESCRIPTION"    AS "STATE_DESCRIPTION"

	
FROM "INSTANCE"

JOIN "INSTANCE_LOCATION" ON (
		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"
)

JOIN "LOCATION" ON (
		"INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"
)

LEFT JOIN "ANSWER"  "DOSSIERNR" ON (
		"DOSSIERNR"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
		AND
		"DOSSIERNR"."QUESTION_ID" = 6
		AND
		"DOSSIERNR"."CHAPTER_ID" = 2
		AND
		"DOSSIERNR"."ITEM" = 1
	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN
	"ANSWER" "ANSWER_STREET_BG" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_BG"."INSTANCE_ID"
		AND
		"ANSWER_STREET_BG"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_BG"."CHAPTER_ID" = 21
		AND
		"ANSWER_STREET_BG"."ITEM" = 1
	)
LEFT JOIN
	"ANSWER" "ANSWER_STREET_NP" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_NP"."INSTANCE_ID"
		AND
		"ANSWER_STREET_NP"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_NP"."CHAPTER_ID" = 101
		AND
		"ANSWER_STREET_NP"."ITEM" = 1
	)

join "FORM" ON (
	"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
)

JOIN "USER" ON (
		"INSTANCE"."USER_ID" = "USER"."USER_ID"
)
LEFT JOIN
	"INSTANCE_STATE_DESCRIPTION" ON (
		"INSTANCE_STATE_DESCRIPTION"."INSTANCE_STATE_ID" = "INSTANCE"."INSTANCE_STATE_ID"
	)

JOIN
	"FORM_GROUP_FORM" ON (
	"FORM_GROUP_FORM"."FORM_ID" = "INSTANCE"."FORM_ID"
)

WHERE
	([ROLE_ID] = 3 AND "FORM_GROUP_FORM"."FORM_GROUP_ID" = 30)
	OR
	([ROLE_ID] = 1061 AND "FORM_GROUP_FORM"."FORM_GROUP_ID" = 141)
	OR
	([ROLE_ID] NOT IN (3, 1061))
