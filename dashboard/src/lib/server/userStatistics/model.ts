import { varchar, serial, pgTable, integer, date, numeric } from "drizzle-orm/pg-core";
import { users } from "../users/model";

export const userStatistic = pgTable('userstatistic',
{
    id: serial('id').primaryKey(),
    user: numeric('user_id').references(() => users.id, {onDelete: 'cascade'}).notNull(),
    sendMessagesCount: numeric('sendMessagesCount'),
    receivedMessagesCount:  numeric('receivedMessagesCount'),
    recipientCounts: numeric('recipientCounts'),
    bccCount: numeric('bccCount'),
    ccCount: numeric('ccCount'),
    daysBetweenReceivedAndRead: numeric('daysBetweenReceivedAndRead'),
    repliedMessagesCount: numeric('repliedMessagesCount'),
    sentCharactersCount: numeric('sentCharactersCount'),
    messagesOutsideWorkingHours: numeric('messagesOutsideWorkingHours'),
    receivedToSentRatio: numeric('receivedToSentRatio'),
    bytesReceivedToSentRatio: numeric('bytesReceivedToSentRatio'),
    messagesWithQuestionAndNoReply: numeric('messagesWithQuestionAndNoReply'),
    readMessagesMoreThan4Hours: numeric('readMessagesMoreThan4Hours'),
    dismissalProbability: numeric('dismissalprobability'),
    startInterval: date('startInterval'),
    endInterval: date('endInterval')
})
    